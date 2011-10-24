import string, random
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings

def generate_invite_code():
    num_chars = getattr(settings, 'BETA_INVITE_CODE_LENGTH', 8)
    return ''.join(random.choice(string.letters) for i in xrange(num_chars))

class InvitationCode(models.Model):
    code = models.CharField(_(u"Invitation code"), blank=True, max_length=8, unique=True)
    is_used = models.BooleanField(_(u"Is Used"), default=False)
    is_invited = models.BooleanField(_('Is Invited'), default=False)
    
    email = models.EmailField(_('Email address'), unique=True)
    user = models.ForeignKey(User, blank=True, null=True, default=None)
    
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    invited = models.DateTimeField(_(u"Invited"), blank=True, null=True)
    used = models.DateTimeField(_(u"Used"), blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_invite_code()
        super(InvitationCode, self).save(*args, **kwargs)