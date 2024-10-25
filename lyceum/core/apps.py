import django.apps

__all__ = ["CoreConfig"]


class CoreConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Приложение с абстрактным классом модели"
