#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.id, ext)
    import os
    return os.path.join('portraits/', filename)

class UserTag(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签名')
    ref_count = models.IntegerField(verbose_name="引用次数", default=0)

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)       

    tags = models.ManyToManyField(UserTag)
    real_name = models.CharField(max_length=20, verbose_name='真实姓名', null=True)
    portrait = models.ImageField(upload_to=get_file_path, null=True, blank=True, verbose_name='头像', default='portraits/default.jpg')
    
    def add_tag(self, tag_name=None, tag_id=None):
        if tag_id:
            tag = UserTag.objects.get(id=tag_id)
        elif tag_name and tag_name != "":
            tag, created = UserTag.objects.get_or_create(name=tag_name)            
        else:
            return
        if self.tags.filter(id=tag.id).exists() == False:
            tag.ref_count += 1
            tag.save()
            self.tags.add(tag)
      
    def remove_tag(self, tag_id):
        tag = UserTag.objects.get(id=tag_id)
        tag.ref_count -= 1
        tag.save()
        self.tags.remove(tag)
