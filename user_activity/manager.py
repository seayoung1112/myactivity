#!/usr/bin/pdefaultython
# -*- coding: utf-8 -*-
from models import Invite
from django.core.exceptions import ObjectDoesNotExist

class UserRole:
    def __init__(self, user, activity):
        self.user = user
        self.activity = activity
    
    def get_role(self):
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