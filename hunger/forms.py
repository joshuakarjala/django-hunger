from django import forms
from hunger.models import Invitation, InvitationCode


class InviteSendForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ('email',)


class InvitationCodeAdminForm(forms.ModelForm):
    code = forms.CharField(initial=lambda: InvitationCode.generate_invite_code())
    class Meta:
        model = InvitationCode

