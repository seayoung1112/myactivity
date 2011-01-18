#!/usr/bin/pdefaultython
# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Story(models.Model):
    creator = models.ForeignKey(User, related_name='stories_created')
    name = models.CharField(max_length=50, verbose_name='名称')
    description = models.TextField(verbose_name='描述')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    activity_place = models.CharField(max_length=100, verbose_name='活动地点')
    participants = models.ManyToManyField(User, related_name='stories_participated', blank=True, null=True)
    is_public = models.BooleanField(verbose_name='公开', default=True)
    def __unicode__(self):
        return self.name
    def get_participants(self, number=5):
        return self.participants.all()[:number]
    def get_photos(self, number=5):
        return self.album.all()[:number]
    def get_posts(self):
        return self.posts.all()
    
def get_user_stories(user):
    return Story.objects.filter((Q(creator=user) | Q(participants=user)) & Q(is_public=True)).distinct().order_by('end_time')

    
def get_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "photo.%s" % (ext)
    import os
    return os.path.join('albums/' + str(instance.story.id) + '/', filename)    

class StoryPhoto(models.Model):
    story = models.ForeignKey(Story, related_name="album")
    content = models.ImageField(upload_to=get_photo_path, null=True)
    upload_by = models.ForeignKey(User, related_name="photos_upload")
    upload_date = models.DateTimeField(default=datetime.now())

class StoryPost(models.Model):
    story = models.ForeignKey(Story, related_name="posts")
    content = models.TextField(verbose_name="内容")
    post_by = models.ForeignKey(User)
    post_date = models.DateTimeField(default=datetime.now()) 
    
class StoryInvitation(models.Model):
    to_user = models.ForeignKey(User, related_name='story_Inviting')
    from_user = models.ForeignKey(User, related_name='story_Invited')
    story = models.ForeignKey(Story) 
    class Meta:
        unique_together = ('to_user', 'from_user')