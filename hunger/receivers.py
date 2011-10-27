import datetime
import importlib
from django.conf import settings
from hunger.models import InvitationCode

#send confirmation email to user
def invitation_code_created(sender, email, **kwargs):    
    email_module = importlib.import_module(settings.BETA_EMAIL_MODULE)
    email_function = getattr(email_module, settings.BETA_EMAIL_CONFIRM_FUNCTION)
    email_function(email)        

#send invitation code to user
def invitation_code_sent(sender, email, invitation_code, **kwargs):
    try:
        invitation_code = InvitationCode.objects.get(email=email)
        invitation_code.is_invited = True
        invitation_code.invited = datetime.datetime.now()
        invitation_code.save()
        
        email_module = importlib.import_module(settings.BETA_EMAIL_MODULE)
        email_function = getattr(email_module, settings.BETA_EMAIL_INVITE_FUNCTION)
        email_function(email, invitation_code.code)
        
    except InvitationCode.DoesNotExist:
        pass

#when user with corresponding email has been created then set the code as used.
def invitation_code_used(sender, user, invitation_code, **kwargs):
    try:
        invitation_code = InvitationCode.objects.get(code=invitation_code)
        invitation_code.user = user
        invitation_code.is_used = True
        invitation_code.used = datetime.datetime.now()
        invitation_code.save()
    except InvitationCode.DoesNotExist:
        pass