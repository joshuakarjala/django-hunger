import datetime
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from everplaces.tools.mail.tasks import send_email
from hunger.models import InvitationCode

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
            send_email.delay(email, "You are now invited to join the beta of Everplaces", "http://everplaces/signup/%s/" % code)
            obj.invited = datetime.datetime.now()
            obj.is_invited = True
            obj.save()
        
    
class InvitationCodeAdmin(admin.ModelAdmin):
    """Admin for invitation code"""
    fields = ('code', 'is_used', 'is_invited', 'user', 'email', 'created', 'invited', 'used', )
    readonly_fields = ('code', 'is_used', 'is_invited', 'email', 'user', 'created', 'invited', 'used', )
    list_display = ('code', 'is_used', 'is_invited', 'email', 'user', 'created', 'invited', 'used', )
    list_filter = ('is_used', 'is_invited', )
    actions = [send_invite]

admin.site.register(InvitationCode, InvitationCodeAdmin)
