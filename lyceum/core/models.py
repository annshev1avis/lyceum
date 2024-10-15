from django.db import models


class CoreModel(models.Model):
    id = models.BigAutoField("id", primary_key=True)
    name = models.CharField("Название", max_length=150)
    is_published = models.BooleanField("Опубликовано", default=True)

    class Meta:
        abstract = True
