from django.contrib import admin

from .models import InvitationCode, BlacklistedDomain


class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'time_created', 'time_accepted', 'expired')
    list_display_links = ('code',)
    search_fields = ('code', 'creator', 'acceptor')
    list_filter = ('time_accepted',)
    ordering = ('-time_created',)
    date_hierarchy = 'time_created'


class BlacklistedDomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'enabled')
    list_display_links = ('domain',)
    search_fields = ('domain',)
    list_filter = ('enabled',)
    ordering = ('domain',)


admin.site.register(InvitationCode, InvitationCodeAdmin)
admin.site.register(BlacklistedDomain, BlacklistedDomainAdmin)
