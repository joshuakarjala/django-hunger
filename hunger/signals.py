import importlib
from django.dispatch import Signal
from hunger.utils import setting


invite_sent = Signal(providing_args=['invitation'])


def invitation_code_sent(sender, invitation, **kwargs):
    """Send invitation code to user.

    Invitation could be InvitationCode or Invitation.
    """
    if sender.__name__ == 'Invitation':
        email = invitation.user.email
        code = invitation.code.code
    elif sender.__name__ == 'InvitationCode':
        email = kwargs.pop('email', None)
        code = invitation.code

    bits = setting('HUNGER_EMAIL_INVITE_FUNCTION').rsplit('.', 1)
    module_name, func_name = bits
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    func(email, code, **kwargs)


invite_sent.connect(invitation_code_sent)