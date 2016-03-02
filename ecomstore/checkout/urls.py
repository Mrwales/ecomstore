'''
Created on Feb 6, 2016

@author: wale
'''
from django.conf.urls import include, url,patterns
from ecomstore import settings
from . import views
urlpatterns = patterns('',
                       url(r'^$', views.show_checkout,{'SSL':settings.ENABLE_SSL},name='checkout'),
                       url(r'^receipt/$',views.receipt,{'SSL':settings.ENABLE_SSL},name='receipt'),
                
                       )