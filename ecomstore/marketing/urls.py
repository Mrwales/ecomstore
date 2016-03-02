'''
Created on Feb 28, 2016

@author: wale
'''

from django.conf.urls import url,patterns
from . import views
from django.contrib.sitemaps.views import sitemap
from marketing.sitemap import SITEMAPS

urlpatterns = patterns('',
                       url(r'^robots\.txt$',views.robots),
                       url(r'^sitemap\.xml$',sitemap, {'sitemaps': SITEMAPS},
                           name='django.contrib.sitemaps.views.sitemap'),
                       url(r'^google_base\.xml$', views.google_base),
                       )