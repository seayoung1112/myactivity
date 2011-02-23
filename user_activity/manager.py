#!/usr/bin/pdefaultython
# -*- coding: utf-8 -*-
from models import Invite, Activity
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

class UserRole:
    def __init__(self, user, activity):
        self.user = user
        self.activity = activity
    
    def get_role(self):
        if self.user.is_anonymous():
            return 'stranger'
        if self.activity.invitor == self.user:
            return 'creator'#创建着
        else:
            try:
                invite = Invite.objects.get(activity=self.activity, user=self.user)
                if invite.response == 'Y':
                    return 'participant'#已经参加者
                elif invite.response == 'H':
                    return 'hesitant'#观望者
                elif invite.response in ('U', 'N'):
                    return 'invitee'#被邀请者
                elif invite.response == 'C':
                    return 'uncheck'#待审核者
            except ObjectDoesNotExist:
                pass
            return 'stranger'#陌生人

from celery.decorators import task

@task()
def change_state():
    activity_finished = Activity.objects.filter(state='I', end_time__lt=datetime.now())
    for activity in activity_finished:
        activity.state='O'
        activity.save()
    activity_processing = Activity.objects.filter(state='P', start_time__lt=datetime.now())
    for activity in activity_processing:
        activity.state='I'
        activity.save()    