from django.contrib import admin
from django.core.urlresolvers import reverse
from website.apwan.models.entity import Entity
from website.apwan.models.entity_reference import EntityReference

__author__ = 'Dean Gardiner'


class EntityAdmin(admin.ModelAdmin):
    list_display = (
        'entity_title', 'image', 'suggested_amount',
        'entity_description'
    )

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
