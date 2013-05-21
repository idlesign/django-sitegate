from django.contrib import admin

from .models import InvitationCode


class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'time_created', 'time_accepted', 'expired')
    list_display_links = ('code',)
    search_fields = ('code', 'creator', 'acceptor')
    list_filter = ('time_accepted',)
    ordering = ('-time_created',)
    date_hierarchy = 'time_created'

admin.site.register(InvitationCode, InvitationCodeAdmin)
