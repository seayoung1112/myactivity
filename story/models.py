from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Story(models.Model):
    creator = models.ForeignKey(User, related_name='stories_created')
    name = models.CharField(max_length=50, verbose_name='名称')
    description = models.TextField(verbose_name='描述')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    activity_place = models.CharField(max_length=100, verbose_name='活动地点')
    participants = models.ManyToManyField(User, through='Invite', related_name='stories_participated', blank=True, null=True)
    is_public = models.BooleanField(verbose_name='公开', default=True)
    def __unicode__(self):
        return self.name