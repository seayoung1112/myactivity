from django import forms
from django.forms import ModelForm, Form
from widget import MyDateTimeWidget, MyTimeWidget
from models import Story

class StoryCreateForm(ModelForm):
    class Meta:
        model = Story
        exclude = ('creator', 'participants')
    def __init__(self, *args, **kwargs):
        super(StoryCreateForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget = MyDateTimeWidget()
        self.fields['end_time'].widget = MyDateTimeWidget()