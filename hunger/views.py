from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from hunger.models import InvitationCode
from hunger.forms import InviteRequestForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView


class InvitationCodeCreate(CreateView):
    """
    Allow a user to request an invite at a later date by
    entering their email address.
    """
    template_name='beta/request_invite.html'
    form_class = InviteRequestForm
    success_url = reverse_lazy('beta_confirmation')


class ConfirmationView(TemplateView):
    """
    Display a message to the user after the invite request is completed
    successfully.
    """
    template_name='beta/confirmation.html'


class UsedView(TemplateView):
    """
    Display a message to the user that the invitation code has already been used.
    """
    template_name='beta/used.html'


def verify_invite(request, invitation_code):
    valid, exists = InvitationCode.validate_code(invitation_code)

    if exists:
        if not valid:
            return redirect('beta_used')
        else:
            url = getattr(settings, 'BETA_SIGNUP_URL', '/register/')
            response = redirect(url)
            response.set_cookie('invitation_code', invitation_code)
            return response
    else:
        url = getattr(settings, 'BETA_REDIRECT_URL', '/beta/')
        return redirect(url)
