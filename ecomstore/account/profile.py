'''
Created on Feb 13, 2016

@author: wale
'''
from account.models import UserProfile
from account.forms import UserprofileForm


def retrieve(request):
    ''' note that this requires an authenticated user before we try calling it '''
    try:
        profile=request.user.profile
    except UserProfile.DoesNotExist:
        profile=UserProfile(user=request.user)
        profile.save()
    return profile

def set(request):
    profile=retrieve(request)
    profile_form=UserprofileForm(request.POST,instance=profile)
    profile_form.save()
    