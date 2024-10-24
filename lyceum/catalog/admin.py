from django.contrib import admin

import catalog.models


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.main_image_tmb,
    ]
    list_editable = [catalog.models.Item.is_published.field.name]
    list_display_links = [catalog.models.Item.name.field.name]
    filter_horizontal = (catalog.models.Item.tags.field.name,)


admin.site.register(catalog.models.Tag)
admin.site.register(catalog.models.Category)
admin.site.register(catalog.models.ImageModel)
