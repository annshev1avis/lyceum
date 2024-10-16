import django.db


class CoreModel(django.db.models.Model):
    id = django.db.models.BigAutoField("id", primary_key=True)
    name = django.db.models.CharField("Название", max_length=150)
    is_published = django.db.models.BooleanField("Опубликовано", default=True)

    class Meta:
        abstract = True
