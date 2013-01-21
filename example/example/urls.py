from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', 'example.views.home', name='home'),
    url(r'^hunger/', include('hunger.urls')),
    url(r'^accounts/profile/$', 'example.views.profile', name='profile'),
)
