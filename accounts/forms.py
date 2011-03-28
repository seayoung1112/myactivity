#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms

class UserRegisterForm(forms.Form):
    realname = forms.CharField(label='真实姓名')
    username = forms.EmailField(label='邮箱')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)