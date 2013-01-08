from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^logged_in_only/$', direct_to_template,
        {'template': 'default.html'}, name='logged_in_only'),
    url(r'^never-allow/$', 'tests.views.never_allow', name='never_allow'),
    url(r'^always-allow/$', 'tests.views.always_allow', name='always_allow'),
    url(r'^always-allow-module/$', 'tests.always_allow_views.allowed',
        name='always_allow_module'),
    url(r'^always-allow-url/$', TemplateView.as_view(template_name='default.html'),
        name='always_allow_url'),
    url(r'^beta/$', direct_to_template,
        {'template': 'default.html'}, name='not_allowed_redirect'),
    url(r'^register/$', 'tests.views.signup', name='register'),
    url(r'^signup-confirmation/$', 'tests.views.signup_confirmation', name='signup_confirmation'),
    url(r'', include('hunger.urls')),
    )
