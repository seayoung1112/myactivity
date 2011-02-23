#!/usr/bin/pdefaultython
# -*- coding: utf-8 -*-
from user_activity.models import Activity, Invite
from django.db.models import Q

def get_user_stories(user):
    return Activity.objects.filter(Q(invitee=user) | Q(invitor=user)).filter(state='O').distinct().order_by('create_time')
    
def get_story_invite(to_user):
    return Invite.objects.filter(user=to_user, response='U')