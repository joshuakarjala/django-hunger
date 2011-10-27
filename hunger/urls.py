from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'hunger.views.invite', name='beta_invite'),
    url(r'^sent', 'hunger.views.confirmation', name='beta_confirmation'),
    url(r'^expired', 'hunger.views.expired', name='beta_used'),
)
