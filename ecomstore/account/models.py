from django.contrib.auth.models import User
from django.db import models

from checkout.models import BaseOrderInfo


# Create your models here.
class UserProfile(BaseOrderInfo):
    user=models.OneToOneField(User,related_name='profile')
    
    def __str__(self):
        return 'User Profile for '+self.user.username