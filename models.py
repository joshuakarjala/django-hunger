import datetime, string, random
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings

def generate_invite_code():
    num_chars = getattr(settings, 'BETA_INVITE_CODE_LENGTH', 8)
    return ''.join(random.choice(string.letters) for i in xrange(num_chars))

class InvitationCode(models.Model):
    """Invitation code model"""
    code = models.CharField(blank=True, max_length=8, unique=True, verbose_name=_(u"Invitation code"))
    is_used = models.BooleanField(default=False, verbose_name=_(u"Is code used?"))
    email = models.EmailField(_('Email address'), unique=True)
    user = models.ForeignKey(User, blank=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    invited = models.BooleanField(_('Invited'), default=False)
    used = models.DateTimeField(blank=True, null=True, default=False, verbose_name=_(u"Used on"))
    
    def save(self, *arg, **kwargs):
        if not self.code:
            self.code = generate_invite_code()