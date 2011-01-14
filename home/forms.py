#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms

class SuggestionForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea, label="内容")