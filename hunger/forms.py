from django import forms
from hunger.models import Invitation

class InviteSendForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ('email',)
