from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()
import haystack

haystack.autodiscover()

urlpatterns = patterns('',
                       (r'^book/', include('book.urls')),
                       (r'^accounts/', include('registration.urls')),
                       (r'^box/', include('box.urls')),
                       (r'^mcq/', include('mcq.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^search/', include('haystack.urls')),
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}),
                            )
