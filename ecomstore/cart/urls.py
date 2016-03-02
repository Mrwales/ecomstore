'''
Created on Jan 24, 2016

@author: wale
'''

from django.conf.urls import url,patterns
from . import views
urlpatterns = patterns('',
                       url(r'^$', views.show_cart, name='show_cart'),
                       )