import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
import transliterate

__all__ = ["CoreModel", "ImageModel"]


ONLY_LETTERS_REGEX = re.compile(r"[^\w]")


class ManagerActive(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class CoreModel(models.Model):
    objects = models.Manager()
    active = ManagerActive()

    name = models.CharField(
        "название",
        max_length=150,
        unique=True,
        help_text="Введите уникальное название",
    )
    is_published = models.BooleanField(
        "опубликовано",
        default=True,
        help_text="Элемент будет виден пользователям",
    )
    canonical_name = models.CharField(
        "каноническое название",
        max_length=150,
        unique=True,
        null=True,
        editable=False,
        help_text="Каноническое название элемента",
    )

    def _generate_canonical_name(self):
        try:
            transliterated = transliterate.translit(
                self.name.lower(),
                reversed=True,
            )
        except transliterate.exceptions.LanguageDetectionError:
            transliterated = self.name.lower()

        return ONLY_LETTERS_REGEX.sub("", transliterated)

    def save(self, *args, **kwargs):
        self.canonical_name = self._generate_canonical_name()
        super().save(*args, **kwargs)

    def clean(self):
        self.canonical_name = self._generate_canonical_name()
        if (
            type(self)
            .objects.filter(canonical_name=self.canonical_name)
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError("Объект с таким именем уже существует")

    class Meta:
        abstract = True


class ImageModel(models.Model):
    image = models.ImageField(
        "изображение товара",
        upload_to="catalog/",
    )

    def get_image_x1280(self):
        return get_thumbnail(self.image, "x1280", quality=51)

    def get_image_x300(self):
        return get_thumbnail(self.image, "x300", quality=51)

    def get_image_x50(self):
        return get_thumbnail(self.image, "x50", quality=51)

    class Meta:
        abstract = True
