from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from hunger.models import InvitationCode
from hunger.signals import invite_sent
from hunger.receivers import invitation_code_sent

#setup signal
invite_sent.connect(invitation_code_sent)

def send_invite(self, request, queryset):
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
            invite_sent.send(sender=self.__class__, email=email, invitation_code=code)
            
def resend_invite(self, request, queryset):
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
            invite_sent.send(sender=self.__class__, email=email, invitation_code=code)
        
    
class InvitationCodeAdmin(admin.ModelAdmin):
    """Admin for invitation code"""
    #fields = ('code', 'is_used', 'is_invited', 'user', 'email', 'created', 'invited', 'used', )
    #readonly_fields = ('code', 'is_used', 'is_invited', 'email', 'user', 'created', 'invited', 'used', )
    list_display = ('code', 'is_used', 'is_invited', 'email', 'user', 'created', 'invited', 'used', )
    list_filter = ('is_used', 'is_invited', 'created', 'invited', 'used')
    search_fields = ['email']
    actions = [send_invite, resend_invite]

admin.site.register(InvitationCode, InvitationCodeAdmin)