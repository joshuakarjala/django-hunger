from django.shortcuts import redirect
from hunger.models import InvitationCode
from hunger.forms import InviteSendForm
from hunger.utils import setting, now
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView


class InviteView(FormView):
    """
    Allow a user to send invites.
    """
    template_name = 'hunger/request_invite.html'
    form_class = InviteSendForm
    success_url = setting('HUNGER_INVITE_SENT_REDIRECT')

    def form_valid(self, form):
        valid_code = InvitationCode.objects.get(owner=self.request.user,
                                                num_invites__gt=0)
        instance = form.save(commit=False)
        instance.code = valid_code
        instance.invited = now()
        instance.save(send_email=True, request=self.request)

        return super(InviteView, self).form_valid(form)


class NotBetaView(TemplateView):
    """
    Display a message to the user after the invite request is completed
    successfully.
    """
    template_name = 'hunger/not_in_beta.html'


class VerifiedView(TemplateView):
    """
    Display a message to the user after the invite request is completed
    successfully.
    """
    template_name = 'hunger/verified.html'


class InvalidView(TemplateView):
    """
    Display a message to the user that the invitation code is
    invalid or has already been used.
    """
    template_name = 'hunger/invalid.html'


class InviteSentView(TemplateView):
    """
    Display a message to the user after sending out invitations to people.
    """
    template_name = 'hunger/invite_sent.html'


def verify_invite(request, code):
    """Verify new invitee by storing invite code for middleware to validate."""
    response = redirect(setting('HUNGER_VERIFIED_REDIRECT'))
    response.set_cookie('hunger_code', code)
    return response
