import importlib
from django.dispatch import Signal
from hunger.utils import setting


invite_created = Signal(providing_args=['invitation'])
invite_sent = Signal(providing_args=['invitation'])


def invitation_created(sender, invitation, **kwargs):
    """Send signup confirmation email to user for self signups.

    Sender should always be Invitation instance.
    """
    email_module_name = setting('HUNGER_EMAIL_MODULE', 'hunger.email')
    email_module = importlib.import_module(email_module_name)
    email_function_name = setting('HUNGER_EMAIL_CONFIRM_FUNCTION', 'beta_confirm')
    email_function = getattr(email_module, email_function_name)
    email_function(invitation.user.email, **kwargs)


def invitation_code_sent(sender, invitation, **kwargs):
    """Send invitation code to user.

    Invitation could be InvitationCode or Invitation."""

    if sender.__name__ == 'Invitation':
        email = invitation.user.email
        code = invitation.code.code
    elif sender.__name__ == 'InvitationCode':
        email = kwargs.pop('email', None)
        code = invitation.code


    email_module_name = setting('HUNGER_EMAIL_MODULE', 'hunger.email')
    email_module = importlib.import_module(email_module_name)
    email_function_name = setting('HUNGER_EMAIL_INVITE_FUNCTION', 'beta_invite')
    email_function = getattr(email_module, email_function_name)
    email_function(email, code, **kwargs)


invite_created.connect(invitation_created)
invite_sent.connect(invitation_code_sent)