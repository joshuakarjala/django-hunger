from django import forms
from hunger.models import Invitation

class InviteRequestForm(forms.ModelForm):
    class Meta:
        model = Invitation
