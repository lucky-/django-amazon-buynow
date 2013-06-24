from django.conf.urls import patterns, url
from amazon_buttons import  views

urlpatterns = patterns('',
    url(r'^$', views.ipn_handler, name='ipn')
)
