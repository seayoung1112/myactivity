#!/usr/bin/python
# -*- coding: utf-8 -*-
from models import Activity, Invite, UserActivityPreference, ActivityType
from django import forms
from django.forms import ModelForm, Form
from widget import MyDateTimeWidget, MyTimeWidget
from datetime import datetime

class ActivityCreateForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ('invitor', 'state', 'invitee', 'create_time')
    def __init__(self, data=None, invitor=None, *args, **kwargs): #必须加data，不然传post数据的时候第一个参数变成invitor了
        super(ActivityCreateForm, self).__init__(data, *args, **kwargs)
        data = data or {}
        self.candidate_times = []
        for key in data.keys():
            if key.startswith('candidate-'):
                time = datetime.strptime(data[key] + ':00', '%Y-%m-%d %H:%M:%S')
                self.candidate_times.append(time)
        if len(self.candidate_times) == 0:
            self.candidate_times = None
        self.fields['start_time'].widget = MyDateTimeWidget()
        self.fields['end_time'].widget = MyDateTimeWidget()

        self.fields['is_public'].widget = forms.RadioSelect(choices = ((True,'公开'), (False,'私有')))
        if invitor is not None:
            self.fields['activity_type'].queryset = ActivityType.objects.filter(useractivitypreference__user=invitor)
        
        
class InviteReplyForm(ModelForm):
    class Meta:
        model = Invite
        exclude = ('user', 'activity')
    def __init__(self, *args, **kwargs):  
        super(InviteReplyForm, self).__init__(*args, **kwargs)
        self.fields['response'].choices = (('Y', '一定参加'), ('W', '尽量参加'), ('H', '犹豫中'), ('N', '不参加'))        
        
class ActivityTypeForm(ModelForm):
    type_name = forms.CharField(label='类型名')
    class Meta:
        model = UserActivityPreference
        fields = ('type_name', 'default_name','default_description', 'default_start_time',
                  'default_duration', 'default_activity_place', 
                  )
        exclude = ('user', 'activity_type')
    def __init__(self, *args, **kwargs):  
        super(ActivityTypeForm, self).__init__(*args, **kwargs)
        self.fields['default_start_time'].widget = MyTimeWidget()
    