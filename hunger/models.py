import string, random
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from hunger.utils import setting
from hunger.signals import invite_created, invite_sent

class Invitation(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    email = models.EmailField(_('Email'), blank=True, null=True)
    code = models.ForeignKey('InvitationCode', blank=True, null=True)
    used = models.DateTimeField(_('Used'), blank=True, null=True)
    invited = models.DateTimeField(_('Invited'), blank=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)

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
    private = models.BooleanField(default=True)
    max_invites = models.PositiveIntegerField(
        _('Max number of invitations'), default=1)
    num_invites = models.PositiveIntegerField(
        _('Remaining invitations'), default=1)
    invited_users = models.ManyToManyField(User,
        related_name='invitations', through='Invitation')
    owner = models.ForeignKey(User, related_name='created_invitations',
        blank=True, null=True)


    def __unicode__(self):
        return self.code

    def remaining_invites(self):
        """The number of invites remaining for this code."""
        return max([0, self.num_invites - self.invited_users.count()])

    def generate_invite_code(self):
        return ''.join(random.choice(string.letters) for i in range(16))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_invite_code()
        # self.num_invites = self.max_invites - self.invited_users.count()
        super(InvitationCode, self).save(*args, **kwargs)
