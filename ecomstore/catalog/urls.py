'''
Created on Jan 16, 2016

@author: wale
'''
from django.conf.urls import include, url,patterns
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='catalog_home'),
                       url(r'^category/(?P<category_slug>[-\w]+)/$',
                        views.show_category, name='catalog_category'),
                       url(r'^category/(?P<category_slug>[-\w]+)/(?P<b_slug>[-\w]+)/$',
                        views.show_category_brands, name='category_brand'),
                       url(r'^product/(?P<product_slug>[-\w]+)/$',views.show_product,name='catalog_product'),
                       url(r'^review/product/add/$',views.add_review,name='add_review'),
                       url(r'^tag/product/add/$', views.add_tag,name='add_tag'),
                       url(r'^tag_cloud/$', views.tag_cloud,name='tag_cloud'),
                       url(r'^tag/(?P<tag>[-\w]+)/$', views.tag,name='tag'),
                       )