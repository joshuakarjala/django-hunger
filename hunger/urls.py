from django.conf.urls.defaults import patterns, url
from .views import InvitationCodeCreate, ConfirmationView, UsedView


urlpatterns = patterns('',
    url(r'^verify/(\w+)/$', 'hunger.views.verify_invite', name='beta_verify_invite'),
    url(r'^$', InvitationCodeCreate.as_view(), name='beta_invite'),
    url(r'^sent/$', ConfirmationView.as_view(), name='beta_confirmation'),
    url(r'^expired/$', UsedView.as_view(), name='beta_used'),
)
