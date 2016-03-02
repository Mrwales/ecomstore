'''
Created on Feb 10, 2016

@author: wale
'''
from django.conf.urls import patterns, url

from ecomstore import settings
from . import views
urlpatterns = patterns("",
                      url(r'^register/$', views.register,{ 'SSL': settings.ENABLE_SSL },name='register'),
                      url(r'^my_account/$', views.my_account, name='my_account'),
                      url(r'^order_details/(?P<order_id>[-\w]+)/$',views.order_details,name='order_details'),
                      url(r'^order_info/$', views.order_info,name='order_info'),
                    )

#login view, for the login page, is in the Django source code
urlpatterns += patterns('django.contrib.auth.views',
                        url(r'^login/$', 'login',{'template_name': 'registration/login.html', 'SSL':settings.ENABLE_SSL }, 'login'),
                        url(r'^logout/$', 'logout',{'template_name': 'registration/logout.html', 'SSL':settings.ENABLE_SSL }, 'logout'),
                        )