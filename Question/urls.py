#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static 
import debug_toolbar

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^account/',include('account.urls')),
    url(r'^question/',include('quest.urls')),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^feed/', include('feed.urls')),
    url(r'^notification/', include('notification.urls')),
    #(r'^search/', include('haystack.urls')),
    #url(r'^test/', include('testpp.urls')),
)
handler404='quest.views.server_error'
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




