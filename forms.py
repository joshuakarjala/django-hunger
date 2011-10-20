from django import forms
from beta.models import InvitationCode

class InviteRequestForm(forms.ModelForm):
    class Meta:
        model = InvitationCode
        fields = ['email']
