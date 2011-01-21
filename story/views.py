#!/usr/bin/pdefaultython
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from forms import StoryForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from models import Story, StoryInvitation, StoryPhoto, StoryPost
from friends.models import friend_set_for
from django.contrib.auth.models import User
from django.http import HttpResponse
from settings import SITE_URL
from helper import send_mail

@login_required
def home(request):
    user = request.user
    stories = list(user.stories_created.all()) + list(user.stories_participated.all())
    return render_to_response('story/list.html', {'stories': stories,})

@login_required
def create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():       
            story = form.save(False)
            story.creator = request.user
            story.save()
            return redirect('/story/edit/' + str(story.id))

            
    else:
        form = StoryForm()
    return render_to_response('story/create.html', {'form': form,}, 
                              context_instance=RequestContext(request))

@login_required   
def edit(request, story_id):#only the invitor can modify it
    user = request.user
    story = Story.objects.get(id=story_id)
    if story.creator == user:
        if request.method == 'POST':
            form = StoryForm(request.POST, instance=story)
            if form.is_valid():            
                form.save()
        else:
            form = StoryForm(instance=story)
        participant_set = set(story.participants.all())
        all_users = set(User.objects.exclude(id=user.id).exclude(is_staff=True).filter(privacy__allow_stranger_invite = True)) - participant_set
        friends = friend_set_for(user) - participant_set        
        return render_to_response('story/edit.html', {'form': form, 'story_id': story_id, 
                                                         'friends': friends, 'participants': story.participants.all(),
                                                         'all_users': all_users,
                                                         'invite_action': '/story/invite/'+story_id+'/'},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponse('you are not permit to do this!')

@login_required
def invite(request, story_id):    
    if request.method == 'GET':
        invitations = StoryInvitation.objects.filter(to_user=request.user, story__id=story_id)
        return render_to_response('story/invitation.html', {'invitations': invitations})
    recipients_list = []
    story = Story.objects.get(pk=story_id)
    for key in request.POST.keys():
        if key.startswith('user_') and request.POST[key] == 'on':
            user_id = key[5:]
            user = User.objects.get(pk=user_id)                
            invite, created = StoryInvitation.objects.get_or_create(to_user=user, from_user=request.user, story=story)
            if created:
                recipients_list.append(invite.to_user.email)
    if request.POST.get('email_notify', default='off') == 'on':
        title = u'来自' + request.user.profile.real_name + u'的邀请'
        invite_url = SITE_URL + 'story/invite/' + story_id
        mail_context = u'您的好友' + request.user.profile.real_name + u'邀请您参加故事' + story.name + u'请到' + invite_url + u' 查看'
        
        try:
            send_mail(title, mail_context, request.user.email, recipients_list, html=mail_context)
            #return HttpResponse(recipients_list)
        except:
            return HttpResponse('email server error!')
                
    return redirect('/story/edit/' + story_id)

@login_required
def agree(request, invite_id):
    invitation = StoryInvitation.objects.get(id=invite_id)
    if request.user != invitation.to_user:
        return HttpResponse("you are not permitted to do this!")
    invitation.story.participants.add(request.user)
    invitation.delete()
    return redirect('/home')
    
@login_required
def ignore(request, invite_id):
    invitation = StoryInvitation.objects.get(id=invite_id)
    if request.user != invitation.to_user:
        return HttpResponse("you are not permitted to do this!")
    invitation.delete()
    return redirect('/home')

def detail(request, story_id):
    story = Story.objects.get(id=story_id)
    return render_to_response('story/detail.html', {'story': story}, context_instance=RequestContext(request))

@login_required
def upload_photo(request, story_id):
    if request.method == "POST":
        story = Story.objects.get(id=story_id)
        StoryPhoto.objects.create(story=story, content=request.FILES['photo'], upload_by=request.user)
        return redirect('/story/detail/' + story_id)
    
@login_required
def post(request, story_id):
    if request.method == "POST":
        story = Story.objects.get(id=story_id)
        StoryPost.objects.create(story=story, content=request.POST['content'], post_by=request.user)
        return redirect('/story/detail/' + story_id)