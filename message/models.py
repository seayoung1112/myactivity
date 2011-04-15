#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Message(models.Model):
    to_user = models.ForeignKey(User, related_name='message_get', verbose_name='收件人')
    from_user = models.ForeignKey(User, related_name='message_send')
    title = models.CharField(max_length=50, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')
    readed = models.BooleanField(default=False)
    MESSAGE_TYPE=(('SYSTEM', '系统'),('USER', '用户'))
    type = models.CharField(choices=MESSAGE_TYPE, max_length=10)
    def __unicode__(self):
        return self.content
    
def send_message(from_user, form=None, **kwargs):
    if form == None: 
        message = Message.objects.create(to_user=kwargs['to_user'], from_user=kwargs['from_user'], 
                                     content=kwargs['content'], type=kwargs['type'])
    else:
        message = form.save(False)
        message.from_user = from_user
        message.type = 'USER'
        message.save()