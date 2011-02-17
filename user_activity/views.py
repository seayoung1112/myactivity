#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, redirect
from forms import ActivityCreateForm, ActivityEditForm, InviteReplyForm, ActivityTypeForm
from models import Activity, Invite, ActivityType, UserActivityPreference
from django.http import HttpResponse
from django.template import RequestContext
from helper import send_mail
from settings import SITE_URL
from friends.models import FriendInvitation, friend_set_for
from profile.models import UserTag

@login_required
def home(request):
    user = request.user    
    activities_invited = user.ac_invitee.filter(id__in=Invite.objects.filter(user=user, response='U').values_list('activity')).order_by('start_time').reverse()
    activities_participated = user.ac_invitee.filter(id__in=Invite.objects.filter(user=user, response='Y').values_list('activity')).order_by('start_time').reverse()
    activities_applied = user.ac_invitee.filter(id__in=Invite.objects.filter(user=user, response='C').values_list('activity')).order_by('start_time').reverse()
    activities_wait = user.ac_invitee.filter(id__in=Invite.objects.filter(user=user, response='H').values_list('activity')).order_by('start_time').reverse()
    activities_quit = user.ac_invitee.filter(id__in=Invite.objects.filter(user=user, response='N').values_list('activity')).order_by('start_time').reverse()

    activities_created = user.ac_invitor.all().order_by('start_time').reverse()
    return render_to_response('activity/list.html', {'activities_created': activities_created,
                                                      'activities_invited': activities_invited,
                                                      'activities_participated': activities_participated,
                                                      'activities_applied': activities_applied,
                                                      'activities_wait': activities_wait,
                                                      'activities_quit': activities_quit,})

@login_required
def create(request):
    if request.method == 'POST':
        form = ActivityCreateForm(request.POST)
        if form.is_valid():       
            new_activity = form.save(False)
            new_activity.invitor = request.user
            new_activity.save()
            return redirect('/activity/home/')

            
    else:
        form = ActivityCreateForm(invitor=request.user)
    return render_to_response('activity/create.html', {'form': form,}, 
                              context_instance=RequestContext(request))
    
@login_required   
def detail(request, activity_id):
    user = request.user
    activity = Activity.objects.get(pk=activity_id)
    from manager import UserRole
    role = UserRole(user, activity).get_role()
    actions = {}
    if role is 'creator':
        actions['邀请'] = '/activity/invite/' + activity_id
        actions['编辑'] = '/activity/edit/' + activity_id
        applicant = Invite.objects.filter(activity=activity, response='C').count()
        if applicant > 0:
            actions['审核申请(' + str(applicant) + ')'] = '/activity/check/' + activity_id
    elif role is 'participant':
        actions['退出'] = '/activity/quit/' + activity_id
        if activity.allow_invitee_invite == True:
            actions['邀请'] = '/activity/invite/' + activity_id
    elif role is 'uncheck':
        actions['撤回申请'] = '/activity/quit/' + activity_id
    elif role is 'invitee':        
        actions['不参加'] = '/activity/quit/' + activity_id
        actions['观望'] = '/activity/wait/' + activity_id
        actions['参加'] = '/activity/join/' + activity_id
    elif role is 'hesitant':        
        actions['不参加'] = '/activity/quit/' + activity_id     
        actions['参加'] = '/activity/join/' + activity_id   
    elif role is 'stranger':
        if activity.is_public:     
            actions['我要参加'] = '/activity/apply/' + activity_id       
        else:
            return HttpResponse('对不起，您无权查看此私有活动')  
    return render_to_response('activity/detail.html', {'actions':actions, 'activity': activity})
    
@login_required   
def edit(request, activity_id):#only the invitor can modify it
    user = request.user
    activity = Activity.objects.get(pk=activity_id)
    if activity.invitor == user:
        if request.method == 'POST':
            form = ActivityCreateForm(request.POST, instance=activity)
            if form.is_valid():            
                form.save()
                return redirect('/activity/detail/' + activity_id)
        else:
            form = ActivityCreateForm(instance=activity, invitor=activity.invitor)
        
        return render_to_response('activity/edit.html', {'form': form, 'activity_id': activity_id,},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponse('you are not the invitor!')
        
@login_required
def invite(request, activity_id):    
    if request.method == 'GET':
        return render_to_response('share/invite.html', { 'id': activity_id,
                                                 'invite_action': '/activity/invite/' + activity_id + '/'},
                          context_instance=RequestContext(request))
    user_from = request.user
    activity = Activity.objects.get(pk=activity_id)
    if not (user_from == activity.invitor or (user_from in activity.person_joined() and activity.allow_invitee_invite)):
        return redirect(u'/error?message=您不能邀请其他人加入次活动')
    recipients_list = []
    for key in request.POST.keys():
        if key.startswith('user_') and request.POST[key] == 'on':
            user_id = key[5:]
            user = User.objects.get(pk=user_id)                
            invite = Invite.objects.create(user=user, activity=activity, response='U')
            if invite is not None:
                recipients_list.append(invite.user.email)
    if request.POST.get('email_notify', default='off') == 'on':
        title = u'来自' + request.user.profile.real_name + u'的邀请'
        invite_url = SITE_URL + 'activity/reply/' + activity_id
        mail_context = u'您的好友' + user_from.profile.real_name + u'邀请您参加' + activity.name + u'请到' + invite_url + u' 查看'
        
        try:
            send_mail(title, mail_context, request.user.email, recipients_list, html=mail_context)
            #return HttpResponse(recipients_list)
        except:
            return HttpResponse('email server error!')
                
    return redirect('/activity/detail/' + activity_id)

@login_required
def quit(request, activity_id):
    try:
        invite = Invite.objects.get(user=request.user, activity__id=activity_id)
        if invite.response == 'C':
            invite.delete()
        else:
            invite.response = 'N'
            invite.save()
        return redirect('/activity/detail/' + activity_id)
    except ObjectDoesNotExist:
        pass
    return redirect(u'/error?message=您还未加入或申请本活动')

@login_required
def join(request, activity_id):
    try:
        invite = Invite.objects.get(user=request.user, activity__id=activity_id)
        if invite.response in ('H', 'U', 'N'):
            invite.join()
            return redirect('/activity/detail/' + activity_id)
    except ObjectDoesNotExist:
        pass
    return redirect(u'/error?message=您未被邀请或审核')

@login_required
def wait(request, activity_id):
    try:
        invite = Invite.objects.get(user=request.user, activity__id=activity_id)
        if invite.response in ('U', 'N'):
            invite.response = 'H'
            invite.save()
            return redirect('/activity/detail/' + activity_id)
    except ObjectDoesNotExist:
        pass
    return redirect(u'/error?message=您目前的状态无法变为观望')

@login_required
def apply(request, activity_id):
    activity = Activity.objects.get(pk=activity_id)
    if activity.is_public == True:
        invite = Invite.objects.create(user=request.user, activity=activity, response='C')
        if activity.need_approve == False:
            invite.join()
    else:
        return redirect(u'/error?message=非公开活动不能申请')
    return redirect('/activity/detail/' + activity_id)
                

@login_required
def check(request, activity_id):
    if not Activity.objects.filter(id=activity_id, invitor=request.user).exists():        
        return redirect(u'/error?message=您不是这个活动的创建者')
    applicant = request.GET.get('applicant',-1)
    if applicant != -1:
        res = request.GET['res']
        try:
            invite = Invite.objects.get(activity__id=activity_id, user__id=applicant, response='C')
        except ObjectDoesNotExist:
            return redirect(u'/error?message=不存在这个活动申请')
        if res == 'ac':
            invite.join()
        elif res == 'neg':
            invite.delete()
        else:
            return redirect(u'/error?message=对申请的操作有错误')
        return redirect('/activity/check/' + activity_id)
            
    applications = Invite.objects.filter(activity__id=activity_id, response='C')
    return render_to_response('activity/check.html', {'applications':applications, 'id':activity_id})
            
    
@login_required
def create_type(request):
    if request.method == "POST":
        form = ActivityTypeForm(request.POST)
        if form.is_valid():
            activity_type, created = ActivityType.objects.get_or_create(name=form.cleaned_data['type_name'])
            if created == False and UserActivityPreference.objects.filter(user=request.user, activity_type=activity_type).exists():
                return HttpResponse('您已设置过此类型，请勿重复设置！')
            preference = form.save(False)
            preference.user = request.user
            preference.activity_type = activity_type
            preference.save()
            return redirect('/activity/create')
    form = ActivityTypeForm()
    return render_to_response('activity/create_type.html', {'form': form},
                              context_instance=RequestContext(request))

import simplejson
import datetime
@login_required
def get_type_default(request, type_id):
    try:
        preference = UserActivityPreference.objects.get(user=request.user, activity_type__id=type_id)
    except:
        return HttpResponse(None)
    start_time = datetime.datetime.combine(datetime.date.today(), preference.default_start_time)
    assembling_time = start_time - datetime.timedelta(minutes=preference.default_assembling_time)
    end_time = start_time + datetime.timedelta(minutes=int(preference.default_duration * 60))
    data = {'name': preference.default_name, 'description': preference.default_description,
            'start_time': str(start_time),
            'assembling_time': str(assembling_time), 
            'end_time': str(end_time), 
            'activity_place': preference.default_activity_place, 
            'assembling_place':preference.default_assembling_place}
    res = simplejson.dumps(data)
    return HttpResponse(res)
    
@login_required
def set_type_default(request):
    if request.method == "POST":
        form = ActivityCreateForm(request.POST)
        if form.is_valid():
            preference = UserActivityPreference.objects.get(user=request.user, activity_type=form.cleaned_data['activity_type'])
            preference.default_name = form.cleaned_data['name']
            preference.default_description = form.cleaned_data['description']
            preference.default_start_time = form.cleaned_data['start_time'].time()
            preference.default_assembling_time = (form.cleaned_data['start_time'] - form.cleaned_data['assembling_time']).seconds / 60
            preference.default_duration = str((form.cleaned_data['end_time'] - form.cleaned_data['start_time']).seconds / float(3600))
            preference.default_activity_place = form.cleaned_data['activity_place']
            preference.default_assembling_place = form.cleaned_data['assembling_place']
            preference.save()
            return HttpResponse('已设为默认')

    return HttpResponse('error!')
from django.core.paginator import *

@login_required
def get_friend_candidates(request, activity_id):
    user = request.user
    activity = Activity.objects.get(pk=activity_id)
    invitee_set = set(activity.invitee.all())
    friend_set = (friend_set_for(user) - invitee_set)
    friend_set.discard(activity.invitor)
    friend_list = list(friend_set)
    paginator = Paginator(friend_list, 10)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        friends = paginator.page(page)
    except (EmptyPage, InvalidPage):
        friends = paginator.page(paginator.num_pages)

    return render_to_response('share/candidates_page.html', {'users': friends})

@login_required
def get_potential_candidates(request, activity_id):
    user = request.user
    activity = Activity.objects.get(pk=activity_id)
    invitee_set = set(activity.invitee.all())
    users = set(User.objects.exclude(id=user.id).exclude(is_staff=True).filter(privacy__allow_stranger_invite = True)) - invitee_set
    users.discard(activity.invitor)
    return render_to_response('share/candidates.html', {'users': users})