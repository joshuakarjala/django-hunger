from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^invited-only/$', 'tests.views.invited_only', name='invited_only'),
    url(r'^always-allow/$', 'tests.views.always_allow', name='always_allow'),
    url(r'^always-allow-module/$', 'tests.always_allow_views.allowed',
        name='always_allow_module'),
    url(r'^not-allowed/$', 'tests.views.rejection', name='rejection'),
    url(r'^hunger/', include('hunger.urls')),
)
