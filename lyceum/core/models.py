import django.db


class CoreModel(django.db.models.Model):
    id = django.db.models.BigAutoField("id", primary_key=True)
    name = django.db.models.CharField(
        "название",
        max_length=150,
        unique=True,
        help_text="Введите уникальное имя",
    )
    is_published = django.db.models.BooleanField(
        "опубликовано",
        default=True,
        help_text="Элемент будет виден пользователям",
    )

    class Meta:
        abstract = True
