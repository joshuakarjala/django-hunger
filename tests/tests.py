from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from hunger import forms
from hunger.utils import setting
from hunger.models import InvitationCode

class BetaViewTests(TestCase):
    urls = 'tests.urls'

    redirect_url = setting('BETA_REDIRECT_URL', '/beta/')
    signup_url = setting('BETA_SIGNUP_URL', '/register/')
    signup_confirmation_view = setting('BETA_SIGNUP_CONFIRMATION_VIEW', '')

    def test_request_invite(self):
        """ Requesting an invite should generate a form and correct template."""
        response = self.client.get(reverse('beta_invite'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'beta/request_invite.html')
        self.failUnless(isinstance(response.context['form'],
                                   forms.InviteRequestForm))

    def test_request_invite_success(self):
        response = self.client.post(reverse('beta_invite'),
                                    data={'email': 'test@example.com'})
        self.assertRedirects(response, reverse('beta_confirmation'))

    def test_never_allow_view(self):
        response = self.client.get(reverse('never_allow'))
        self.assertRedirects(response, self.redirect_url)

    def test_always_allow_view(self):
        response = self.client.get(reverse('always_allow'))
        self.assertEqual(response.status_code, 200)

    def test_always_allow_module(self):
        response = self.client.get(reverse('always_allow_module'))
        self.assertEqual(response.status_code, 200)

    def test_garden_when_not_logged_in(self):
        response = self.client.get(reverse('logged_in_only'))
        self.assertRedirects(response,
                             reverse('beta_invite') + '?next=%s' % reverse('logged_in_only'))

    def test_garden_when_logged_in(self):
        User.objects.create_user('alice', 'alice@example.com', 'secret')
        self.client.login(username='alice', password='secret')
        response = self.client.get(reverse('logged_in_only'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_using_invite(self):
        invitation = InvitationCode(email='alice@example.com')
        invitation.save()
        response = self.client.get(reverse('beta_verify_invite', args=[invitation.code]))
        self.assertRedirects(response, self.signup_url)
        User.objects.create_user('alice', 'alice@example.com', 'secret')
        self.client.login(username='alice', password='secret')
        response = self.client.get(reverse(self.signup_confirmation_view))
        response = self.client.get(reverse('beta_verify_invite', args=[invitation.code]))
        self.assertRedirects(response, reverse('beta_used'))

    def test_invalid_invite(self):
        code = 'xoxoxoxo'
        with self.assertRaises(InvitationCode.DoesNotExist):
            InvitationCode.objects.get(code=code)
        response = self.client.get(reverse('beta_verify_invite', args=[code]))
        self.assertRedirects(response, self.redirect_url)
