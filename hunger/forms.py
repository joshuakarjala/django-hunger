from __future__ import unicode_literals
from django import forms
from hunger.models import Invitation, InvitationCode


class InviteSendForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(InviteSendForm, self).__init__(*args, **kwargs)

        # When sending an invitation, the email address is required
        self.fields['email'].required = True


class InvitationCodeAdminForm(forms.ModelForm):
    code = forms.CharField(
        initial=lambda: InvitationCode.generate_invite_code())

    class Meta:
        model = InvitationCode
