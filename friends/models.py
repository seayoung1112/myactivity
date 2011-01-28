#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from managers import FriendshipManager
import datetime

class Friendship(models.Model):
    """
    A friendship is a bi-directional association between two users who
    have both agreed to the association.
    """
    
    to_user = models.ForeignKey(User, related_name="friends")
    from_user = models.ForeignKey(User, related_name="_unused_")
    # @@@ relationship types
    added = models.DateField(default=datetime.date.today)
    
    objects = FriendshipManager()
    
    class Meta:
        unique_together = [("to_user", "from_user")]
        
def friend_set_for(user):
    return set([obj["friend"] for obj in Friendship.objects.friends_for_user(user)])

class FriendInvitation(models.Model):
    from_user = models.ForeignKey(User, related_name='friends_applying')
    to_user = models.ForeignKey(User, related_name='friends_applied') 
    message = models.TextField(null=True, blank=True)
    class Meta:
        unique_together = ('from_user', 'to_user')