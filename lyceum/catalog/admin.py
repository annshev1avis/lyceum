import django.contrib.admin

import catalog.models


class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = ["name", "is_published"]
    list_editable = ["is_published"]
    list_display_links = ["name"]
    filter_horizontal = ("tags",)


django.contrib.admin.site.register(catalog.models.Item, ItemAdmin)
django.contrib.admin.site.register(catalog.models.Tag)
django.contrib.admin.site.register(catalog.models.Category)
