from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
    url(r'^invited-only/$', direct_to_template,
        {'template': 'default.html'}, name='invited_only'),
    url(r'^always-allow/$', 'tests.views.always_allow', name='always_allow'),
    url(r'^always-allow-module/$', 'tests.always_allow_views.allowed',
        name='always_allow_module'),
    url(r'^not-allowed/$', 'tests.views.rejection', name='rejection'),
    url(r'^hunger/', include('hunger.urls')),
)
