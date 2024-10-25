import django.apps

__all__ = ["CatalogConfig"]


class CatalogConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"
    verbose_name = "Каталог"
