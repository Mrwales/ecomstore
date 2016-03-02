'''
Created on Feb 13, 2016

@author: wale
'''
from django import forms

from account.models import UserProfile


class UserprofileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)