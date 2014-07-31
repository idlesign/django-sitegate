from django.contrib import admin

from .models import InvitationCode, BlacklistedDomain, EmailConfirmation


class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'time_created', 'time_accepted', 'expired')
    list_display_links = ('code',)
    search_fields = ('code', 'creator', 'acceptor')
    list_filter = ('time_accepted',)
    ordering = ('-time_created',)
    date_hierarchy = 'time_created'
admin.site.register(InvitationCode, InvitationCodeAdmin)


class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('code', 'time_created', 'time_accepted', 'expired')
    list_display_links = ('code',)
    search_fields = ('code', 'user')
    list_filter = ('time_accepted',)
    ordering = ('-time_created',)
    date_hierarchy = 'time_created'
admin.site.register(EmailConfirmation, EmailConfirmationAdmin)


class BlacklistedDomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'enabled')
    list_display_links = ('domain',)
    search_fields = ('domain',)
    list_filter = ('enabled',)
    ordering = ('domain',)
admin.site.register(BlacklistedDomain, BlacklistedDomainAdmin)
