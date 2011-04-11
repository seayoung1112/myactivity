#!/usr/bin/pdefaultython
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from forms import StoryForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from friends.models import friend_set_for
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from user_activity.models import get_user_activity, Activity, ActivityPhoto, ActivityPost, Invite
from models import get_story_invite
from settings import SITE_URL
from helper import send_mail
import datetime

@login_required
def home(request):
    user = request.user
    activities = get_user_activity(user).filter(state='O')
    return render_to_response('story/list.html', {'activities': activities,})

@login_required
def create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():       
            story = form.save(False)
            story.invitor = request.user
            story.state = 'O'
            story.save()
            return redirect('/story/detail/' + str(story.id))            
    else:
        try:
            year = int(request.GET['year'])
            month = int(request.GET['month'])
            day = int(request.GET['day'])
            start_time = datetime.datetime(year, month, day)
            form = StoryForm(initial={'start_time':start_time})
        except:            
            form = StoryForm()
    return render_to_response('story/create.html', {'form': form,}, 
                              context_instance=RequestContext(request))

@login_required   
def edit(request, story_id):#only the invitor can modify it    
    user = request.user
    story = Activity.objects.get(id=story_id)
    if story.invitor == user:
        if request.method == 'POST':
            form = StoryForm(request.POST, instance=story)
            if form.is_valid():            
                form.save()
        else:
            form = StoryForm(instance=story)  
        return render_to_response('story/edit.html', {'form': form, 'story_id': story_id,},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponse('you are not permit to do this!')

@login_required
def invite(request, story_id):    
    if request.method == 'GET':
        tabs = {}
        tabs['好友'] = '/story/friend-candidates/story_id/?page=1'
        return render_to_response('share/invite.html', { 'id': story_id,
                                                 'type': 'story',
                                                 'tabs': tabs,},
                          context_instance=RequestContext(request))
    recipients_list = []
    story = Activity.objects.get(pk=story_id)
    for key in request.POST.keys():
        if key.startswith('user_') and request.POST[key] == 'on':
            user_id = key[5:]
            user = User.objects.get(pk=user_id)   
            try:
                invite = Invite.objects.create(user=user, activity=story, response='U')             
                recipients_list.append(invite.to_user.email)
            except:
                pass
    if request.POST.get('email_notify', default='off') == 'on':
        title = u'来自' + request.user.profile.real_name + u'的邀请'
        invite_url = SITE_URL + 'story/invite/' + story_id
        mail_context = u'您的好友' + request.user.profile.real_name + u'邀请您参加故事' + story.name + u'请到' + invite_url + u' 查看'
        
        try:
            send_mail(title, mail_context, request.user.email, recipients_list, html=mail_context)
            #return HttpResponse(recipients_list)
        except:
            return HttpResponse('email server error!')
                
    return redirect('/story/detail/' + story_id)#('/story/edit/' + story_id)

@login_required
def invitation(request):
    invitations = get_story_invite(request.user)
    return render_to_response('story/invitation.html', {'invitations': invitations})


@login_required
def agree(request, invite_id):
    invitation = Invite.objects.get(id=invite_id)
    if request.user != invitation.user:
        return HttpResponse("you are not permitted to do this!")
    invitation.response = 'Y'
    invitation.save()
    return redirect('/story/detail/' + str(invitation.activity.id))
    
@login_required
def ignore(request, invite_id):
    invitation = Invite.objects.get(id=invite_id)
    if request.user != invitation.user:
        return HttpResponse("you are not permitted to do this!")
    invitation.delete()
    return redirect('/story/invitation')

def detail(request, story_id):
    story = Activity.objects.get(id=story_id)
    users = story.person_joined()
    return render_to_response('story/detail.html', {'story': story,
                                                    'users': users,},
                                                     context_instance=RequestContext(request))

@login_required
def upload_photo(request, story_id):
    if request.method == "POST":
        story = Activity.objects.get(id=story_id)
        try:
            ActivityPhoto.objects.create(activity=story, content=request.FILES['photo'], upload_by=request.user)
        except:
            pass
        return redirect('/story/detail/' + story_id)
    
@login_required
def post(request, story_id):
    if request.method == "POST":
        story = Activity.objects.get(id=story_id)
        ActivityPost.objects.create(activity=story, content=request.POST['content'], post_by=request.user)
        return redirect('/story/detail/' + story_id)
    
@login_required
def get_participants(request, story_id):
    story = Activity.objects.get(id=story_id)
    users = story.person_joined()
    return render_to_response('share/user_list.html', {"users": users})