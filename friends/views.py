#!/usr/bin/pdefaultython
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from profile.models import Profile, User
from models import FriendInvitation, Friendship, friend_set_for
from django.template import RequestContext
from django.http import HttpResponse
from story.models import get_user_stories
from user_activity.models import get_user_activity

@login_required
def list(request):
    user = request.user
    friend_list = friend_set_for(user)
    return render_to_response('friends/list.html',{'friends': friend_list})
    
@login_required
def add(request, user_id):
    friend = User.objects.get(id=user_id)
    invitation, created = FriendInvitation.objects.get_or_create(from_user=request.user, to_user=friend)
    invitation.message = request.POST.get("message", "")
    invitation.save()
    return HttpResponse("已发送请求")

@login_required
def invitation(request):
    invitation = FriendInvitation.objects.filter(to_user=request.user)
    return render_to_response('friends/invitation.html', {'friend_invitations': invitation})

@login_required
def agree(request, app_id):
    invitation = FriendInvitation.objects.get(id=app_id)
    if request.user != invitation.to_user:
        return HttpResponse("you are not permitted to do this!")
    friendship = Friendship.objects.get_or_create(to_user=invitation.from_user, from_user=invitation.to_user)
    if friendship is not None:
        invitation.delete()
    return redirect('/friends/invitation')
    
@login_required
def ignore(request, app_id):
    invitation = FriendInvitation.objects.get(id=app_id)
    if request.user != invitation.to_user:
        return HttpResponse("you are not permitted to do this!")
    invitation.delete()
    return redirect('/friends/invitation')


def user_info(request, user_id):
    user = User.objects.get(id=user_id)
    if user == request.user:
        return redirect('/home')
    activities = get_user_activity(user)
    stories = get_user_stories(user)
    return render_to_response('user/user_info.html', {'user': user, "activities": activities, 'stories': stories,})