import datetime
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User


DEFAULT_SETTINGS = {
    'AUTH_USER_MODEL': User,
    'HUNGER_ENABLE': True,
    'HUNGER_ALWAYS_ALLOW_VIEWS': [],
    'HUNGER_ALWAYS_ALLOW_MODULES': [],
    'HUNGER_REDIRECT': reverse_lazy('hunger-not-in-beta'),
    'HUNGER_VERIFIED_REDIRECT': reverse_lazy('hunger-verified'),
    'HUNGER_INVITE_SENT_REDIRECT': reverse_lazy('hunger-invite-sent'),
    'HUNGER_ALLOW_FLATPAGES': [],
    'HUNGER_EMAIL_TEMPLATES_DIR': 'hunger',
    'HUNGER_EMAIL_INVITE_FUNCTION': 'hunger.email.beta_invite',
}


def setting(name):
    """Return setting value for given name or default value."""
    return getattr(settings, name, None) or DEFAULT_SETTINGS[name]


def now():
    """Backwards compatible now function when USE_TZ=False."""
    if getattr(settings, 'USE_TZ'):
        from django.utils import timezone
        return timezone.now()
    else:
        return datetime.datetime.now()
