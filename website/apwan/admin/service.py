from django.contrib import admin
from website.apwan.models.service import Service

__author__ = 'Dean Gardiner'


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'service', 'service_type', 'service_id',
        'link_type', 'email'
    )
    list_display_links = ('service_id',)
    exclude = ('data',)

    def email(self, obj):
        return obj.email()
admin.site.register(Service, ServiceAdmin)
