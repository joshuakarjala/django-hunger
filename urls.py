from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'beta.views.invite', name='beta_invite'),
    url(r'^sent/$', 'beta.views.confirmation', name='beta_confirmation'),
    url(r'^expired/$', 'beta.views.expired', name='beta_expired'),
)
