#!/usr/bin/pdefaultython
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class ActivityType(models.Model):
    name = models.CharField(max_length=100, verbose_name='类型名', unique=True)
    def __unicode__(self):
        return self.name
    
class UserActivityPreference(models.Model):
    user = models.ForeignKey(User)
    activity_type = models.ForeignKey(ActivityType)
    default_name = models.CharField(max_length=50, verbose_name='默认活动名')
    default_description = models.TextField(verbose_name='活动介绍')
    default_start_time = models.TimeField(verbose_name='默认开始时间')
    default_assembling_time = models.IntegerField(verbose_name=r'默认多少时间前集合（分钟）')
    default_duration = models.DecimalField(verbose_name=r'默认持续时间(小时)', max_digits=4, decimal_places=1)    
    default_activity_place = models.CharField(max_length=100, verbose_name='默认活动地点')
    default_assembling_place = models.CharField(max_length=100, verbose_name='默认集合地点')
    class Meta:
        unique_together = ('user', 'activity_type')
    
def get_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "photo.%s" % (ext)
    import os
    return os.path.join('albums/' + str(instance.activity.id) + '/', filename)
    
def get_cover_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "photo.%s" % (ext)
    import os
    return os.path.join('covers/', filename)   
    
class Activity(models.Model):
    invitor = models.ForeignKey(User, related_name='ac_invitor')
    name = models.CharField(max_length=50, verbose_name='标题')
    image = models.ImageField(default='images/default_album.png', upload_to=get_cover_photo_path, null=True, blank=True, verbose_name="活动封面")
    activity_type = models.ForeignKey(ActivityType, verbose_name='类型', null=True)    
    description = models.TextField(verbose_name='活动介绍')
    start_time = models.DateTimeField(verbose_name='开始时间')
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.now)
    end_time = models.DateTimeField(verbose_name='结束时间')
    assembling_time = models.DateTimeField(verbose_name='集合时间', blank=True, null=True)
    activity_place = models.CharField(max_length=100, verbose_name='活动地点')
    assembling_place = models.CharField(max_length=100, verbose_name='集合地点', blank=True, null=True)
    invitee = models.ManyToManyField(User, through='Invite', related_name='ac_invitee', blank=True, null=True)
    ACTIVITY_STATE_CHOICES = (('P','筹备'), ('I','进行中'), ('O', '已结束'), ('C', '已取消'))
    is_public = models.BooleanField(verbose_name='公开性', default=True)
    need_approve = models.BooleanField(verbose_name='申请需要审核', default=False)
    allow_invitee_invite = models.BooleanField(verbose_name='允许活动成员邀请Ta的朋友', default=True)
    state = models.CharField(max_length=2, choices=ACTIVITY_STATE_CHOICES, verbose_name='状态', default='P')
    def __unicode__(self):
        return self.name
    def person_invited(self):
        return self.invitee.filter(invite__response='U')
    def person_joined(self):
        return self.invitee.filter(invite__response='Y')
    def person_declined(self):
        return self.invitee.filter(invite__response='N')
    def person_wait(self):
        return self.invitee.filter(invite__response='H')
    def is_public_display(self):
        if self.is_public:
            return '公开活动'
        else:
            return '私有活动'
    def get_photos(self):
        return self.album.all()
    def get_posts(self):
        return self.posts.all()

from django.db.models import Q
def get_user_activity(user):
    #此处查询需要加上distinct，因为or是用left outer join处理，一个acitivity会对应多个invitee，从而有多条符合invitor的结果，导致重复
    return Activity.objects.filter(Q(invitee=user) | Q(invitor=user)).distinct().order_by('create_time')
    
class Invite(models.Model):
    RESPONSE_TYPES = (('Y', '参加'), ('H', '观望'), ('N', '不参加'), ('U', '未阅读'), ('C', '待审核'))
    response = models.CharField(max_length=2, choices=RESPONSE_TYPES, verbose_name='回复')
    user = models.ForeignKey(User)
    activity = models.ForeignKey(Activity)
    class Meta:
        unique_together = ('user', 'activity')
    def join(self):
        self.response = 'Y'
        self.save()
        if not UserActivityPreference.objects.filter(user=self.user, activity_type=self.activity.activity_type).exists():
            try:
                preference = UserActivityPreference.objects.get(user=self.activity.invitor, activity_type=self.activity.activity_type)
                preference.id = None
                preference.user = self.user
                preference.save()
            except:
                pass
            
class ActivityPhoto(models.Model):
    activity = models.ForeignKey(Activity, related_name="album")
    content = models.ImageField(upload_to=get_photo_path, null=True)
    upload_by = models.ForeignKey(User, related_name="photos_upload")
    upload_date = models.DateTimeField(default=datetime.now)

class ActivityPost(models.Model):
    activity = models.ForeignKey(Activity, related_name="posts")
    content = models.TextField(verbose_name="内容")
    post_by = models.ForeignKey(User)
    post_date = models.DateTimeField(default=datetime.now) 