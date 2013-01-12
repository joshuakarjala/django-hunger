from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
    url(r'^logged_in_only/$', direct_to_template,
        {'template': 'default.html'}, name='logged_in_only'),
    url(r'^never-allow/$', 'tests.views.never_allow', name='never_allow'),
    url(r'^always-allow/$', 'tests.views.always_allow', name='always_allow'),
    url(r'^always-allow-module/$', 'tests.always_allow_views.allowed',
        name='always_allow_module'),
    url(r'^view-by-name/1/$', TemplateView.as_view(template_name='default.html'),
        name='allow_me'),
    url(r'^view-by-name/2/$', TemplateView.as_view(template_name='default.html'),
        name='deny_me'),
    url(r'^view-with-no-name/$', TemplateView.as_view(template_name='default.html')),
    url(r'^beta/$', direct_to_template,
        {'template': 'default.html'}, name='not_allowed_redirect'),
    url(r'^register/$', 'tests.views.signup', name='register'),
    url(r'^signup-confirmation/$', 'tests.views.signup_confirmation', name='signup_confirmation'),
    url(r'', include('hunger.urls')),
    )
