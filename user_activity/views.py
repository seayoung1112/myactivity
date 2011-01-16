#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from forms import ActivityCreateForm, ActivityEditForm, InviteReplyForm, ActivityTypeForm
from models import Activity, Invite, ActivityType, UserActivityPreference
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from helper import send_mail
from settings import SITE_URL
from friends.models import FriendApplication, friend_set_for
from profile.models import UserTag
from story.models import Story

# Create your views here.
@login_required
def home(request):
    user = request.user
    activities_invited = user.ac_invitee.filter(id__in=Invite.objects.filter(user=user).exclude(response='U').values_list('activity'))
    activities_created = user.ac_invitor.all()
    stories = list(user.stories_created.all()) + list(user.stories_participated.all())
    unhandled_invite = Invite.objects.filter(user=user, response='U')
    friend_application_count = FriendApplication.objects.filter(apply_object=user).count()
    hot_tags = UserTag.objects.all()
    return render_to_response('user/index.html', {'user': user, 'activities_created': activities_created,
                                                  'activities_invited': activities_invited,   
                                                  'unhandled_invite': unhandled_invite,
                                                  'friend_application_count': friend_application_count,
                                                  'stories': stories,
                                                  'hot_tags': hot_tags,},
                                                  context_instance=RequestContext(request))
    
@login_required
def create(request):
    if request.method == 'POST':
        form = ActivityCreateForm(request.POST)
        if form.is_valid():       
            new_activity = form.save(False)
            new_activity.invitor = request.user
            new_activity.save()
            return redirect('/activity/edit/' + str(new_activity.id))

            
    else:
        form = ActivityCreateForm(invitor=request.user)
    return render_to_response('activity/create.html', {'form': form,}, 
                              context_instance=RequestContext(request))
    
@login_required   
def detail(request, activity_id):
    user = request.user
    activity = Activity.objects.get(pk=activity_id)
    if activity.invitor == user:
        return HttpResponseRedirect('/activity/edit/' + activity_id)
    elif user in activity.invitee.all():
        return HttpResponseRedirect('/activity/reply/' + str(activity_id))
    elif activity.is_public:
        return redirect('/activity/apply/' + activity_id)        
    
@login_required   
def edit(request, activity_id):#only the invitor can modify it
    user = request.user
    activity = Activity.objects.get(pk=activity_id)
    if activity.invitor == user:
        if request.method == 'POST':
            form = ActivityCreateForm(request.POST, instance=activity)
            if form.is_valid():            
                form.save()
        else:
            form = ActivityCreateForm(instance=activity, invitor=activity.invitor)
        invitee_set = set(activity.invitee.all())
        all_users = set(User.objects.exclude(id=user.id).exclude(is_staff=True).filter(privacy__allow_stranger_invite = True)) - invitee_set
        friends = friend_set_for(user) - invitee_set
        
        #candidates = set(User.objects.exclude(pk=user.id).exclude(is_staff=True)) - set(activity.invitee.all())#I think this can be improved
        invites = Invite.objects.filter(activity__id__exact=activity_id)
        return render_to_response('activity/edit.html', {'form': form, 'activity_id': activity_id, 
                                                         'friends': friends, 'invites': invites,
                                                         'all_users': all_users,
                                                         'invite_action': '/activity/invite/'+activity_id+'/'},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponse('you are not the invitor!')
        
@login_required
def invite(request, activity_id):    
    if request.method == 'GET':
        return redirect('/activity/edit/' + activity_id)
    recipients_list = []
    activity = Activity.objects.get(pk=activity_id)
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
        mail_context = u'您的好友' + request.user.profile.real_name + u'邀请您参加' + activity.name + u'请到' + invite_url + u' 查看'
        
        try:
            send_mail(title, mail_context, request.user.email, recipients_list, html=mail_context)
            #return HttpResponse(recipients_list)
        except:
            return HttpResponse('email server error!')
                
    return HttpResponseRedirect('/activity/edit/' + activity_id)

@login_required
def reply(request, activity_id):
    activity = Activity.objects.get(pk=activity_id)
    invite = Invite.objects.get(user=request.user, activity=activity)
    if invite is not None:
        if request.method == 'POST':
            form = InviteReplyForm(request.POST, instance=invite)
            if form.is_valid():
                invite = form.save()
                if invite.response in ['Y', 'W']:
                    if ~UserActivityPreference.objects.filter(user=request.user, activity_type=activity.activity_type).exists():
                        preference = UserActivityPreference.objects.get(user=activity.invitor, activity_type=activity.activity_type)
                        preference.id = None
                        preference.user = request.user
                        preference.save()
                return redirect('/home/')
            else:
                return HttpResponse('something wrong!')
        else:
            form = InviteReplyForm(instance=invite)
        return render_to_response('activity/reply.html', {'form': form, 'invite': invite},
                                  context_instance=RequestContext(request))
    return HttpResponse('you can not access this page!')
            
    
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