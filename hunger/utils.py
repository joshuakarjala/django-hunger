from django.conf import settings

def setting(name, default=None):
    """Return setting value for given name or default value."""
    return getattr(settings, name, default)
