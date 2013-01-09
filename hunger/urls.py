from django.conf.urls.defaults import patterns, url
from .views import InviteView, ConfirmationView, UsedView


urlpatterns = patterns('',
    url(r'^verify/(\w+)/$', 'hunger.views.verify_invite', name='hunger_verify'),
    url(r'^invite/$', InviteView.as_view(), name='hunger_invite'),
    url(r'^sent/$', ConfirmationView.as_view(), name='hunger_confirmation'),
    url(r'^expired/$', UsedView.as_view(), name='hunger_used'),
)
