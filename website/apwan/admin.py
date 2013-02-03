from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from website.apwan.models.donation import Donation
from website.apwan.models.entity import Entity
from website.apwan.models.entity_reference import EntityReference
from website.apwan.models.payee import Payee
from website.apwan.models.recipient import Recipient
from website.apwan.models.recipient_reference import RecipientReference
from website.apwan.models.service import Service
from website.apwan.models.user_profile import UserProfile

__author__ = 'Dean Gardiner'


class DonationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Donation, DonationAdmin)


class EntityAdmin(admin.ModelAdmin):
    list_display = ('entity_title', 'image', 'suggested_amount', 'entity_description')

    def entity_title(self, obj):
        return obj.__unicode__()
    entity_title.short_description = 'Title'

    def entity_description(self, obj):
        return obj.description()
    entity_description.short_description = 'Description'

admin.site.register(Entity, EntityAdmin)


class EntityReferenceAdmin(admin.ModelAdmin):
    list_display = ('entity_link', 'type', 'key')
    list_display_links = ('key',)

    def entity_link(self, obj):
        url = reverse('admin:apwan_entity_changelist')
        return '<a href="%s?id=%s">%s</a>' % (url, obj.entity_id, obj.entity)
    entity_link.allow_tags = True
admin.site.register(EntityReference, EntityReferenceAdmin)


class PayeeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'slug', 'user_link')
    list_display_links = ('name',)

    def user_link(self, obj):
        if obj.user is None:
            return obj.user
        url = reverse('admin:apwan_service_changelist')
        return '<a href="%s?id=%s">%s</a>' % (url, obj.user_id, obj.user)
    user_link.short_description = "User"
    user_link.allow_tags = True
admin.site.register(Payee, PayeeAdmin)


class RecipientAdmin(admin.ModelAdmin):
    list_display = ('type', 'title', 'slug')
    list_display_links = ('title',)
admin.site.register(Recipient, RecipientAdmin)


class RecipientReferenceAdmin(admin.ModelAdmin):
    list_display = ('recipient_link', 'type', 'key')
    list_display_links = ('key',)

    def recipient_link(self, obj):
        url = reverse('admin:apwan_recipient_changelist')
        return '<a href="%s?id=%s">%s</a>' % (url, obj.recipient_id, obj.recipient)
    recipient_link.allow_tags = True
admin.site.register(RecipientReference, RecipientReferenceAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('owner', 'service', 'service_type', 'service_id', 'link_type', 'email')
    list_display_links = ('service_id',)
    exclude = ('data',)

    def email(self, obj):
        return obj.email()
admin.site.register(Service, ServiceAdmin)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = "user"
    max_num = 1
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)