import string, random
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from hunger.utils import setting
from hunger.signals import invite_created, invite_sent

class Invitation(models.Model):
    user = models.ForeignKey(User)
    code = models.ForeignKey('InvitationCode')
    used = models.DateTimeField(_('Used'), blank=True, null=True)
    invited = models.DateTimeField(_('Invited'), blank=True, null=True)

    @property
    def is_used(self):
        if self.used:
            return True
        return False

    @property
    def is_invited(self):
        if self.invited:
            return True
        return False

    def save(self, *args, **kwargs):
        send_email = kwargs.pop('send_email', False)
        request = kwargs.pop('request', None)
        if send_email and not self.is_invited:
            invite_created.send(sender=self.__class__, invitation=self,
                                request=request, user=self.user)
        if send_email and self.is_invited and not self.is_used:
            invite_sent.send(sender=self.__class__, invitation=self,
                             request=request, user=self.user)
        super(Invitation, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('user', 'code'),)


class InvitationCode(models.Model):
    code = models.CharField(_('Invitation code'), max_length=30, unique=True)
    num_invites = models.PositiveIntegerField(
        _('Number of invitations'), default=1)
    invited_users = models.ManyToManyField(User,
        related_name='invitations', through='Invitation')
    created_by = models.ForeignKey(User, related_name='created_invitations',
        blank=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    def __unicode__(self):
        return self.code

    def remaining_invites(self):
        """The number of invites remaining for this code."""
        return max([0, self.num_invites - self.invited_users.count()])

    @classmethod
    def generate_invite_code(cls):
        num_chars = setting('BETA_INVITE_CODE_LENGTH', 8)
        return ''.join(random.choice(string.letters) for i in range(num_chars))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_invite_code()
        super(InvitationCode, self).save(*args, **kwargs)

    @classmethod
    def validate_code(cls, code):
        """Returns (valid, exists)."""
        try:
            invitation_code = InvitationCode.objects.get(code=code)
            if invitation_code.is_used:
                return False, True
            else:
                return True, True
        except InvitationCode.DoesNotExist:
            return False, False
