#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from user_activity.models import Invite, Activity, ActivityCalendar
from friends.models import FriendInvitation
from story.models import get_story_invite
from story.models import get_user_stories
from user_activity.models import get_user_activity
from profile.models import UserTag
from django.contrib.auth.models import User
from datetime import date
from message.models import Message

@login_required
def home(request):
    user = request.user
    public_activities = Activity.objects.filter(is_public=True, state='P').order_by('create_time').reverse()
    activity_invitation = Invite.objects.filter(user=user, response='U')
    story_invitation = get_story_invite(to_user=user)
    friend_application_count = FriendInvitation.objects.filter(to_user=user).count()
    messages =  Message.objects.filter(to_user=request.user, readed=False)
    cal = ActivityCalendar(date.today().year, date.today().month, user)
    t = get_template('activity/calendar.html')
    c = Context(dict(cal=cal, portrait=user.profile.portrait.url))
    html = t.render(c)
    return render_to_response('user/index.html', {'user': user,
                                                  'public_activities': public_activities[:2],   
                                                  'messages': messages,
                                                  'activity_invitation': activity_invitation,
                                                  "story_invitation": story_invitation,
                                                  'friend_application_count': friend_application_count,
                                                  'calendar_html': html,
                                                  },
                                                  context_instance=RequestContext(request))

def search(request):
    username = request.GET['user_name']
    template = request.GET.get('template', None)
    users = User.objects.filter(profile__real_name__icontains=username)
    if template is None:
        return HttpResponse("no template!")
    return render_to_response(template, {'users': users,},
                              context_instance=RequestContext(request))
        
@login_required
def settings(request):
    pages = {'profile':0, 'password':1, 'tag':2} 
    content = request.GET.get('content', 'profile')
    page = pages[content]
    return render_to_response('user/settings.html', {'page':page},
                              context_instance=RequestContext(request))

def user_info(request, user_id):
    user = User.objects.get(id=user_id)
    if user == request.user:
        return redirect('/home')
    activities = get_user_activity(user)
    stories = get_user_stories(user)
    return render_to_response('user/user_info.html', {'person': user, "activities": activities, 'stories': stories,},
                              context_instance=RequestContext(request))