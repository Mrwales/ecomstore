'''
Created on Feb 14, 2016

@author: wale
'''

from django.conf.urls import patterns,url
from . import views
urlpatterns = patterns('',
                       url(r'^results/$',views.results,name='search_results'),
                       )