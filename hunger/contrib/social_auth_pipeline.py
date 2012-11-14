from django.http import HttpResponseRedirect
from social_auth.utils import setting
from social_auth.models import UserSocialAuth
from hunger.models import InvitationCode
from hunger.signals import invite_used


def create_beta_user(backend, details, response, uid, username, user=None,
                     *args, **kwargs):
    """Create user. Depends on get_username pipeline."""
    if user:
        return {'user': user}
    if not username:
        return None

    if setting('BETA_ENABLE_BETA', True):
        request = kwargs['request']
        invitation_code = request.COOKIES.get('invitation_code', False)
        if not invitation_code:
            return HttpResponseRedirect(setting('BETA_REDIRECT_URL'))
        valid, exists = InvitationCode.validate_code(invitation_code)
        if not valid:
            return HttpResponseRedirect(setting('BETA_REDIRECT_URL'))

    email = details.get('email')
    user = UserSocialAuth.create_user(username=username, email=email)
    if setting('BETA_ENABLE_BETA', True):
        invite_used.send(sender=user, user=user, invitation_code=invitation_code)

    return {
        'user': user,
        'is_new': True
    }
