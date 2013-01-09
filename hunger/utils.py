import datetime
from django.conf import settings


DEFAULT_SETTINGS = {
    'HUNGER_ENABLE': True,
    'HUNGER_ALWAYS_ALLOW_VIEWS': [],
    'HUNGER_ALWAYS_ALLOW_MODULES': [],
    'HUNGER_SIGNUP_VIEWS': [],
    'HUNGER_SIGNUP_CONFIRMATION_VIEW': '',
    'HUNGER_SIGNUP_URL': '/register/',
    'HUNGER_REDIRECT': '/beta/',
    'HUNGER_VERIFIED_REDIRECT': '/beta/',
    'HUNGER_ALLOW_FLATPAGES': [],
    'HUNGER_EMAIL_TEMPLATES_DIR': 'hunger',
    'HUNGER_INVITE_CODE_LENGTH': 8,
    'HUNGER_EMAIL_MODULE': 'hunger.email',
    'HUNGER_EMAIL_CONFIRM_FUNCTION': 'beta_confirm',
    'HUNGER_EMAIL_INVITE_FUNCTION': 'beta_invite',
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
