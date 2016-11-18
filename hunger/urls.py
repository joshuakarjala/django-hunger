from __future__ import unicode_literals
from django.conf.urls import url
from .views import (InviteView, VerifiedView, InvalidView, NotBetaView,
                    InviteSentView, verify_invite)


urlpatterns = [
    url(r'^verify/(\w+)/$', verify_invite, name='hunger-verify'),
    url(r'^invite/$', InviteView.as_view(), name='hunger-invite'),
    url(r'^sent/$', InviteSentView.as_view(), name='hunger-invite-sent'),
    url(r'^not-in-beta/$', NotBetaView.as_view(), name='hunger-not-in-beta'),
    url(r'^verified/$', VerifiedView.as_view(), name='hunger-verified'),
    url(r'^invalid/(?P<code>\w+)/$', InvalidView.as_view(), name='hunger-invalid'),
]
