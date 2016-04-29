from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from hunger.utils import setting, now
from hunger.models import Invitation, InvitationCode

from django.test.utils import override_settings

class BetaViewTests(TestCase):
    urls = 'tests.urls'

    redirect = setting('HUNGER_REDIRECT')

    def create_invite(self, email):
        code = InvitationCode(num_invites=0)
        code.save()
        invitation = Invitation(code=code, email=email, invited=now())
        invitation.save()
        return invitation

    def create_code(self, private=True, email=''):
        code = InvitationCode(private=private)
        code.save()
        if private:
            invitation = Invitation(code=code, email=email, invited=now())
            invitation.save()
        return code

    def setUp(self):
        """Creates a few basic users.

        Alice is registered but not in beta
        Bob is registered and in beta (self-signup)
        Charlie is in beta and has one invite
        """
        self.alice = User.objects.create_user('alice', 'alice@example.com', 'secret')
        self.bob = User.objects.create_user('bob', 'bob@example.com', 'secret')
        right_now = now()
        invitation = Invitation(user=self.bob, invited=right_now, used=right_now)
        invitation.save()

        self.charlie = User.objects.create_user('charlie', 'charlie@example.com', 'secret')
        invitation = Invitation(user=self.charlie, invited=right_now, used=right_now)
        invitation.save()
        code = InvitationCode(owner=self.charlie)
        code.save()

    def test_always_allow_view(self):
        response = self.client.get(reverse('always_allow'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'default.html')

    def test_always_allow_module(self):
        response = self.client.get(reverse('always_allow_module'))
        self.assertEqual(response.status_code, 200)

    def test_garden_when_not_invited(self):
        """
        Confirm that an unauthenticated user is redirected to login.
        """
        response = self.client.get(reverse('invited_only'))
        self.assertRedirects(response, setting('LOGIN_URL')+"?next=/invited-only/")

    def test_using_invite(self):
        cary = User.objects.create_user('cary', 'cary@example.com', 'secret')
        self.client.login(username='cary', password='secret')
        response = self.client.get(reverse('invited_only'))
        self.assertRedirects(response, reverse(self.redirect))

        response = self.client.get(reverse('invited_only'))
        self.assertRedirects(response, reverse(self.redirect))
        invitation = Invitation.objects.get(user=cary)
        invitation.invited = now()
        invitation.save()
        response = self.client.get(reverse('invited_only'))
        self.assertEqual(response.status_code, 200)

    def test_user_invite(self):
        """
        Confirm that one user can invite another to beta.
        """
        self.client.login(username='charlie', password='secret')
        response = self.client.post(reverse('hunger-invite'), {'email': 'cary@example.com'})
        self.assertRedirects(response, reverse('hunger-invite-sent'))
        self.client.logout()

        # @TODO: Replace with examining email body
        User.objects.create_user('cary', 'cary@example.com', 'secret')
        self.client.login(username='cary', password='secret')
        invitation = Invitation.objects.get(email='cary@example.com')
        response = self.client.get(reverse('hunger-verify', args=[invitation.code.code]))
        # Cary should be allowed to verify the code that belongs to her
        self.assertRedirects(response, reverse('hunger-verified'))
        self.client.logout()

        User.objects.create_user('dany', 'dany@example.com', 'secret')
        self.client.login(username='dany', password='secret')
        response = self.client.get(reverse('invited_only'))
        # Dany should be denied, since he has no connection with Cary
        self.assertRedirects(response, reverse('rejection'))

    def test_invite_non_user_with_email(self):
        """
        Confirm that someone invited to beta can later register.
        """
        self.create_invite(email='dany@example.com')
        User.objects.create_user('dany', 'dany@example.com', 'secret')
        self.client.login(username='dany', password='secret')
        response = self.client.get(reverse('invited_only'))
        self.assertEqual(response.status_code, 200)

    def test_invite_existing_user_with_email(self):
        """
        Confirm that existing user can later be invited to beta.
        """
        self.create_invite(email='alice@example.com')
        self.client.login(username='alice', password='secret')
        response = self.client.get(reverse('invited_only'))
        self.assertEqual(response.status_code, 200)

    def test_invite_non_user_without_email(self):
        """
        Confirm that an unregistered user cannot join beta using a private
        InvitationCode meant for someone else.
        """
        code = self.create_code(email='dany1@example.com')
        response = self.client.get(reverse('hunger-verify',
                                           args=[code.code]), follow=True)
        # Anonymous user cannot verify a private InvitationCode
        self.assertRedirects(response, setting('LOGIN_URL')+"?next=/hunger/verified/")

        User.objects.create_user('dany', 'dany@example.com', 'secret')
        self.client.login(username='dany', password='secret')
        response = self.client.get(reverse('invited_only'))
        # Dany should be denied, since he has no connection with email account
        self.assertRedirects(response, reverse('hunger-invalid', args=[code.code]))

    def test_invite_non_user_public_invitation(self):
        """
        Confirm that an unregistered user can join beta using a public
        InvitationCode.
        """
        code = self.create_code(private=False)

        # Anonymous user can verify a public InvitationCode, but cannot
        # access pages behind beta until logged in.
        response = self.client.get(reverse('hunger-verify',
                                           args=[code.code]), follow=True)

        response = self.client.get(reverse('invited_only'))
        self.assertRedirects(response, setting('LOGIN_URL')+"?next=/invited-only/")

        User.objects.create_user('dany', 'dany@example.com', 'secret')
        self.client.login(username='dany', password='secret')
        response = self.client.get(reverse('invited_only'))
        # Dany is allowed in beta since he used public code earlier in session
        self.assertEqual(response.status_code, 200)

    def test_invite_existing_user_without_email(self):
        """
        Confirm that a registered user cannot join beta using a private
        InvitationCode meant for someone else.
        """
        code = self.create_code(email='not_alice@example.com')
        response = self.client.get(reverse('hunger-verify',
                                           args=[code.code]), follow=True)
        # Anonymous user cannot verify a private InvitationCode
        self.assertRedirects(response, setting('LOGIN_URL')+"?next=/hunger/verified/")

        self.client.login(username='alice', password='secret')
        response = self.client.get(reverse('invited_only'))
        # Alice should be denied, since she has no connection with email account
        self.assertRedirects(response, reverse('hunger-invalid', args=[code.code]))

    def test_invalid_code(self):
        """
        Confirm that a registered user cannot join beta using a random code.
        """
        invalid_code = 'XXXXinvalidcodeXXXX'
        self.client.login(username='alice', password='secret')
        response = self.client.get(reverse('hunger-verify',
                                           args=[invalid_code]), follow=True)
        self.assertRedirects(response, reverse('hunger-invalid', args=[invalid_code]))

    @override_settings(HUNGER_ENABLE=False)
    def test_settings(self):
        """
        Confirm that settings override DEFAULT_SETTINGS
        """
        self.assertEqual(False, setting('HUNGER_ENABLE'))
