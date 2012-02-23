import csv
from datetime import datetime
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseForbidden
from hunger.models import InvitationCode
from hunger.signals import invite_sent
from hunger.receivers import invitation_code_sent

#setup signal
invite_sent.connect(invitation_code_sent)

def export_email(self, request, queryset):
    emails = ""
    
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=email.csv'
    writer = csv.writer(response)

    writer.writerow(["email", "is_used", "is_invited", "created", "invited", "used"])
        
    for obj in queryset:
        code = obj
        email = code.email
        is_used = code.is_used
        is_invited = code.is_invited
        created = datetime.strftime(code.created, "%Y-%m-%d %H:%M:%S")
        try:
            invited = datetime.strftime(code.invited, "%Y-%m-%d %H:%M:%S")
        except TypeError:
            invited = ""
        try:
            used = datetime.strftime(code.used, "%Y-%m-%d %H:%M:%S")
        except TypeError:
            used = ""

        if len(email) >0 and email != "None":
            row = [email, is_used, is_invited, created, invited, used]
            row.append(email)
            writer.writerow(row)
    # Return CSV file to browser as download
    return response

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
    actions = [send_invite, resend_invite, export_email]

admin.site.register(InvitationCode, InvitationCodeAdmin)