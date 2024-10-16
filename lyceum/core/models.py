import django.db


class CoreModel(django.db.models.Model):
    id = django.db.models.BigAutoField("id", primary_key=True)
    name = django.db.models.CharField("название", max_length=150, unique=True)
    is_published = django.db.models.BooleanField("опубликовано", default=True)

    class Meta:
        abstract = True
