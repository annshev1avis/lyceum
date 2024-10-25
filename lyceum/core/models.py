from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

__all__ = ["CoreModel", "ImageModel"]


class CoreModel(models.Model):
    name = models.CharField(
        "название",
        max_length=150,
        unique=True,
        help_text="Введите уникальное имя",
    )
    is_published = models.BooleanField(
        "опубликовано",
        default=True,
        help_text="Элемент будет виден пользователям",
    )

    class Meta:
        abstract = True


class ImageModel(models.Model):
    image = models.ImageField(
        "изображение товара",
        upload_to="catalog/",
    )

    def get_image_x1280(self):
        return get_thumbnail(self.image, "1280", quality=51)

    def get_image_300x300(self):
        return get_thumbnail(self.image, "300x300", crop="center", quality=51)

    def image_tmb(self):
        if self.image:
            return mark_safe(
                f"<img src='{self.image.url}' width='50'>",
            )
        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    class Meta:
        abstract = True
