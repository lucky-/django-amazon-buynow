from django.conf.urls import patterns, url
from amazon_buttons import  views

urlpatterns = patterns('',
    url(r'^ipn_handler/', views.handler, name='ipn')
)
