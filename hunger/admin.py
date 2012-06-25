import csv
from datetime import datetime
from django.contrib import admin
from django.http import HttpResponse
from hunger.models import InvitationCode
from hunger.signals import invite_sent
from hunger.receivers import invitation_code_sent


invite_sent.connect(invitation_code_sent)


def export_email(modeladmin, request, queryset):
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


def send_invite(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.is_invited:
            invite_sent.send(sender=modeladmin.__class__, email=obj.email,
                             invitation_code=obj.code,
                             user=obj.user, request=request)


def resend_invite(modeladmin, request, queryset):
    for obj in queryset:
        if obj.is_invited:
            invite_sent.send(sender=modeladmin.__class__, email=obj.email,
                             invitation_code=obj.code,
                             user=obj.user, request=request)


class InvitationCodeAdmin(admin.ModelAdmin):
    """Admin for invitation code"""
    list_display = ('code', 'is_used', 'is_invited', 'email', 'user', 'created', 'invited', 'used', )
    list_filter = ('is_used', 'is_invited', 'created', 'invited', 'used')
    search_fields = ['email']
    actions = [send_invite, resend_invite, export_email]

admin.site.register(InvitationCode, InvitationCodeAdmin)
