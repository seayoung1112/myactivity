#!/usr/bin/pdefaultython
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ActivityType(models.Model):
    name = models.CharField(max_length=100, verbose_name='类型名', unique=True)
    def __unicode__(self):
        return self.name
    
class UserActivityPreference(models.Model):
    user = models.ForeignKey(User)
    activity_type = models.ForeignKey(ActivityType)
    default_name = models.CharField(max_length=50, verbose_name='默认活动名')
    default_description = models.TextField(verbose_name='描述')
    default_start_time = models.TimeField(verbose_name='默认开始时间')
    default_assembling_time = models.IntegerField(verbose_name=r'默认多少时间前集合（分钟）')
    default_duration = models.DecimalField(verbose_name=r'默认持续时间(小时)', max_digits=4, decimal_places=1)    
    default_activity_place = models.CharField(max_length=100, verbose_name='默认活动地点')
    default_assembling_place = models.CharField(max_length=100, verbose_name='默认集合地点')
    class Meta:
        unique_together = ('user', 'activity_type')
    
class Activity(models.Model):
    invitor = models.ForeignKey(User, related_name='ac_invitor')
    activity_type = models.ForeignKey(ActivityType, verbose_name='类型')
    name = models.CharField(max_length=50, verbose_name='名称')
    description = models.TextField(verbose_name='描述')
    start_time = models.DateTimeField(verbose_name='预计开始时间')
    end_time = models.DateTimeField(verbose_name='预计结束时间')
    assembling_time = models.DateTimeField(verbose_name='集合时间')
    activity_place = models.CharField(max_length=100, verbose_name='活动地点')
    assembling_place = models.CharField(max_length=100, verbose_name='集合地点')
    invitee = models.ManyToManyField(User, through='Invite', related_name='ac_invitee', blank=True, null=True)
    ACTIVITY_STATE_CHOICES = (('P','筹备'), ('I','进行中'), ('O', '已结束'), ('C', '已取消'))
    is_public = models.BooleanField(verbose_name='公开', default=True)
    state = models.CharField(max_length=2, choices=ACTIVITY_STATE_CHOICES, verbose_name='状态', default='P')
    def __unicode__(self):
        return self.name
    def person_invited(self):
        return self.invitee.count()
    def person_attended(self):
        return self.invite_set.filter(response__in=['Y','W']).count()
    def person_declined(self):
        return self.invite_set.filter(response = 'N').count()

from django.db.models import Q
def get_user_activity(user):
    #此处查询需要加上distinct，因为or是用left outer join处理，一个acitivity会对应多个invitee，从而有多条符合invitor的结果，导致重复
    return Activity.objects.filter((Q(invitee=user) | Q(invitor=user)) & Q(is_public=True)).distinct().order_by('start_time')
    
class Invite(models.Model):
    RESPONSE_TYPES = (('Y', '一定参加'), ('W', '尽量参加'), ('H', '犹豫中'), ('N', '不参加'), ('U', '未阅读'))
    response = models.CharField(max_length=2, choices=RESPONSE_TYPES, verbose_name='回复')
    user = models.ForeignKey(User)
    activity = models.ForeignKey(Activity)
    class Meta:
        unique_together = ('user', 'activity')