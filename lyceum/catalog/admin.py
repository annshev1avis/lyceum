from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

import catalog.models

__all__ = ["GalleryImagesInline", "ItemAdmin", "MainImageInline"]


class MainImageInline(admin.TabularInline):
    model = catalog.models.MainImage
    max_num = 1


class GalleryImagesInline(admin.TabularInline):
    model = catalog.models.GalleryImage


@admin.register(catalog.models.Item)
class ItemAdmin(SummernoteModelAdmin):
    list_display = [
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        "main_image_preview",
    ]
    list_editable = [catalog.models.Item.is_published.field.name]
    list_display_links = [catalog.models.Item.name.field.name]
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    inlines = [MainImageInline, GalleryImagesInline]
    exclude = ["main_image"]
    summernote_fields = ["text"]

    def main_image_preview(self, obj):
        if obj.main_image:
            return obj.main_image.image_tmb()
        else:
            return "Нет изображения"

    main_image_preview.short_description = "превью"
    main_image_preview.allow_tags = True


admin.site.register(catalog.models.Tag)
admin.site.register(catalog.models.Category)
