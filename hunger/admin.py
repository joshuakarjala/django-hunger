import csv
from datetime import datetime
from django.contrib import admin
from django.http import HttpResponse
from hunger.models import InvitationCode, Invitation
from hunger.utils import now


def export_email(modeladmin, request, queryset):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=email.csv'
    writer = csv.writer(response)

    writer.writerow(['email', 'is_used', 'is_invited', 'created', 'invited', 'used'])

    for obj in queryset:
        code = obj.code
        email = obj.user.email
        used = obj.used
        invited = obj.invited
        created = datetime.strftime(code.created, "%Y-%m-%d %H:%M:%S")
        try:
            invited = datetime.strftime(obj.invited, "%Y-%m-%d %H:%M:%S")
        except TypeError:
            invited = ''
        try:
            used = datetime.strftime(obj.used, "%Y-%m-%d %H:%M:%S")
        except TypeError:
            used = ''

        if email:
            row = [email, created, invited, used]
            writer.writerow(row)
    # Return CSV file to browser as download
    return response


def send_invite(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.invited:
            obj.invited = now()
            obj.save(send_email=True, request=request)


def resend_invite(modeladmin, request, queryset):
    for obj in queryset:
        if obj.invited:
            obj.save(send_email=True, request=request)


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'used', 'invited')
    list_filter = ('code',)
    search_fields = ['user__username', 'user__email']
    actions = [send_invite, resend_invite, export_email]


class InvitationCodeAdmin(admin.ModelAdmin):
    """Admin for invitation code"""
    list_display = ('code', 'num_invites', 'created_by', 'created',  )
    list_filter = ('created', )
    filter_horizontal = ('invited_users', )
    search_fields = ['created_by__email', 'created_by__username']


admin.site.register(Invitation, InvitationAdmin)
admin.site.register(InvitationCode, InvitationCodeAdmin)
