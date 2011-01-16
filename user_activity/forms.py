#!/usr/bin/python
# -*- coding: utf-8 -*-
from models import Activity, Invite, UserActivityPreference, ActivityType
from django import forms
from django.forms import ModelForm, Form
from widget import MyDateTimeWidget, MyTimeWidget

class ActivityCreateForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ('invitor', 'state', 'invitee')
    def __init__(self, data=None, invitor=None, *args, **kwargs): #必须加data，不然传post数据的时候第一个参数变成invitor了
        super(ActivityCreateForm, self).__init__(data, *args, **kwargs)
        self.fields['start_time'].widget = MyDateTimeWidget()
        self.fields['end_time'].widget = MyDateTimeWidget()
        self.fields['assembling_time'].widget = MyDateTimeWidget()
        if invitor is not None:
            self.fields['activity_type'].queryset = ActivityType.objects.filter(useractivitypreference__user=invitor)
        
        
class ActivityEditForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ('invitor', 'state', 'invitee')
    def __init__(self, *args, **kwargs):
        super(ActivityEditForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget = MyDateTimeWidget()
        self.fields['end_time'].widget = MyDateTimeWidget()
        self.fields['assembling_time'].widget = MyDateTimeWidget()
        
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
                  'default_assembling_time', 'default_duration', 'default_activity_place', 
                  'default_assembling_place')
        exclude = ('user', 'activity_type')
    def __init__(self, *args, **kwargs):  
        super(ActivityTypeForm, self).__init__(*args, **kwargs)
        self.fields['default_start_time'].widget = MyTimeWidget()
    