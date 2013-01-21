from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from hunger import forms
from hunger.utils import setting, now
from hunger.models import Invitation, InvitationCode


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

    def test_never_allow_view_by_name(self):
        response = self.client.get(reverse('deny_me'))
        self.assertRedirects(response, self.redirect_url)

    def test_always_allow_view_by_name(self):
        response = self.client.get(reverse('allow_me'))
        self.assertEqual(response.status_code, 200)

    def test_never_allow_view_without_name(self):
        url = '/view-with-no-name/'
        response = self.client.get(url)
        self.assertRedirects(response, '{0}?next={1}'.format(self.redirect_url, url))

    def test_always_allow_module(self):
        response = self.client.get(reverse('always_allow_module'))
        self.assertEqual(response.status_code, 200)

    def test_garden_when_not_invited(self):
        response = self.client.get(reverse('invited_only'))
        self.assertRedirects(response, reverse(self.redirect))

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
        self.client.login(username='charlie', password='secret')
        response = self.client.post(reverse('hunger-invite'), {'email': 'cary@example.com'})
        self.assertEqual(response.status_code, 302)
        self.client.logout()

        # Replace with examining email body
        invitation = Invitation.objects.get(email='cary@example.com')
        self.client.get(reverse('hunger-verify', args=[invitation.code.code]))

        User.objects.create_user('dany', 'dany@example.com', 'secret')
        self.client.login(username='dany', password='secret')
        response = self.client.get(reverse('invited_only'))
        self.assertEqual(response.status_code, 200)

    def test_invite_non_user_with_email(self):
        self.create_invite(email='dany@example.com')
        User.objects.create_user('dany', 'dany@example.com', 'secret')
        self.client.login(username='dany', password='secret')
        response = self.client.get(reverse('invited_only'))
        self.assertEqual(response.status_code, 200)

    def test_invite_existing_user_with_email(self):
        self.create_invite(email='alice@example.com')
        self.client.login(username='alice', password='secret')
        response = self.client.get(reverse('invited_only'))
        self.assertEqual(response.status_code, 200)

    def test_invite_non_user_without_email(self):
        code = self.create_code(email='dany1@example.com')
        self.client.get(reverse('hunger-verify', args=[code.code]))
        User.objects.create_user('dany', 'dany@example.com', 'secret')
        self.client.login(username='dany', password='secret')
        response = self.client.get(reverse('invited_only'))
        self.assertEqual(response.status_code, 200)

    def test_invite_existing_user_without_email(self):
        code = self.create_code(email='alice1@example.com')
        self.client.get(reverse('hunger-verify', args=[code.code]))
        self.client.login(username='alice', password='secret')
        response = self.client.get(reverse('invited_only'))
        self.assertEqual(response.status_code, 200)
