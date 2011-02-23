#!/usr/bin/pdefaultython
# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Form
from widget import MyDateTimeWidget, MyTimeWidget
from user_activity.models import Activity

class StoryForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ('invitor', 'state', 'invitee', 'activity_type', 'assembling_time', 'assembling_place', 'create_time')
    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget = MyDateTimeWidget()
        self.fields['end_time'].widget = MyDateTimeWidget()
        self.fields['is_public'].widget = forms.RadioSelect(choices = ((True,'公开'), (False,'私有')))