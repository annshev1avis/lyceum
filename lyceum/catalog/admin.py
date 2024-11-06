from django.contrib import admin

import catalog.models

__all__ = ["GalleryImagesInline", "ItemAdmin", "MainImageInline"]


class MainImageInline(admin.TabularInline):
    model = catalog.models.MainImage
    max_num = 1


class GalleryImagesInline(admin.TabularInline):
    model = catalog.models.GalleryImage


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
        catalog.models.Item.image_tmb,
    ]
    list_editable = [
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
    ]
    list_display_links = [catalog.models.Item.name.field.name]
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    inlines = [MainImageInline, GalleryImagesInline]
    exclude = ["main_image"]
    readonly_fields = [
        catalog.models.Item.created.field.name,
        catalog.models.Item.updated.field.name,
    ]


admin.site.register(catalog.models.Tag)
admin.site.register(catalog.models.Category)
