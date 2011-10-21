from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from hunger.models import InvitationCode
from hunger.signals import invite_sent
from hunger.receivers import invitation_code_sent

#setup signal
invite_sent.connect(invitation_code_sent)

def send_invite(self, request, queryset):
    import importlib
    email_module = importlib.import_module(settings.BETA_EMAIL_FUNCTION)
    email_function = getattr(email_module, 'beta_email')
    obj = queryset[0]
    email_col = 0
    code_col = 0
    
    for field in obj._meta.fields:
        if field.get_attname() == "email":
            break
        email_col = email_col + 1
        
    for field in obj._meta.fields:
        if field.get_attname() == "code":
            break
        code_col = code_col + 1
    
    for obj in queryset:
        email = obj._meta.fields[email_col].value_to_string(obj)
        code = obj._meta.fields[code_col].value_to_string(obj)
        
        if not obj.is_invited:
            email_function(email, code)
            invite_sent.send(sender=self.__class__, email=email)
            
def resend_invite(self, request, queryset):
    import importlib
    email_module = importlib.import_module(settings.BETA_EMAIL_FUNCTION)
    email_function = getattr(email_module, 'beta_email')
    obj = queryset[0]
    email_col = 0
    code_col = 0
    
    for field in obj._meta.fields:
        if field.get_attname() == "email":
            break
        email_col = email_col + 1
        
    for field in obj._meta.fields:
        if field.get_attname() == "code":
            break
        code_col = code_col + 1
    
    for obj in queryset:
        email = obj._meta.fields[email_col].value_to_string(obj)
        code = obj._meta.fields[code_col].value_to_string(obj)
        
        if obj.is_invited:
            email_function(email, code)
            invite_sent.send(sender=self.__class__, email=email)
        
    
class InvitationCodeAdmin(admin.ModelAdmin):
    """Admin for invitation code"""
    #fields = ('code', 'is_used', 'is_invited', 'user', 'email', 'created', 'invited', 'used', )
    #readonly_fields = ('code', 'is_used', 'is_invited', 'email', 'user', 'created', 'invited', 'used', )
    list_display = ('code', 'is_used', 'is_invited', 'email', 'user', 'created', 'invited', 'used', )
    list_filter = ('is_used', 'is_invited', )
    actions = [send_invite, resend_invite]

admin.site.register(InvitationCode, InvitationCodeAdmin)
