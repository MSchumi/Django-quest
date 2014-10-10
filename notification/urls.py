#coding=utf-8
from django.conf.urls import patterns, include, url


urlpatterns = patterns('notification.views',
    url(r'^read/$', "set_message_read"),
    url(r'^messagelist/$',"get_notifications"),
    url(r'', "get_notification_list"),
)






