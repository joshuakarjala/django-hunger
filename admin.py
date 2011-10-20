from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from beta.models import InvitationCode


class InvitationCodeAdmin(admin.ModelAdmin):
    """Admin for invitation code"""
    fields = ('code', 'is_used', 'user', 'email', 'created', 'invited', 'used', )
    readonly_fields = ('code', 'is_used', 'email', 'user', 'created', 'invited', 'used', )
    list_display = ('code', 'is_used', 'email', 'user', 'created', 'invited', 'used', )
    list_filter = ('is_used', 'used_date', )

admin.site.register(InvitationCode, InvitationCodeAdmin)
