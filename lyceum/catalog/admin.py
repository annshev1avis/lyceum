from django.contrib import admin

import catalog.models


class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "is_published"]
    list_editable = ["is_published"]
    list_display_links = ["name"]
    filter_horizontal = ("tags",)


admin.site.register(catalog.models.Item, ItemAdmin)
admin.site.register(catalog.models.Tag)
admin.site.register(catalog.models.Category)
