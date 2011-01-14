#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Privacy(models.Model):
    allow_stranger_invite = models.BooleanField(verbose_name='允许陌生人邀请', default=True)
    user = models.OneToOneField(User, primary_key=True)