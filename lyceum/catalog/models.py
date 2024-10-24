from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

import catalog.validators
import core.models


class Item(core.models.CoreModel):
    text = models.TextField(
        "текст",
        validators=[
            catalog.validators.ValidateMustContain("превосходно", "роскошно"),
        ],
        help_text="Опишите товар",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="категория",
        help_text="Выберите категорию",
    )
    tags = models.ManyToManyField(
        "Tag",
        related_name="items",
        verbose_name="теги",
        help_text="Можно выбрать несколько тегов",
    )
    main_image = models.OneToOneField(
        "ImageModel",
        on_delete=models.CASCADE,
        verbose_name="главная картинка",
        related_name="item_main",
        null=True,
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return f"{self.name}"

    def main_image_tmb(self):
        if self.main_image:
            return mark_safe(
                f"img src='{self.main_image.image.url} width='50'",
            )
        return "Нет изображения"


class Tag(core.models.CoreModel):
    slug = models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="Слаг может состоять из латинских букв, "
        "цифр и нижнего подчеркивания",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return f"{self.name}"


class Category(core.models.CoreModel):
    slug = models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="Слаг может состоять из латинских букв, "
        "цифр и нижнего подчеркивания",
    )

    weight = models.IntegerField(
        "вес",
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(32767)],
        help_text="Введите число от 1 до 32767",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return f"{self.name}"


class ImageModel(models.Model):
    image = models.ImageField(
        "изображение товара",
        upload_to="catalog/",
    )
    item = models.ForeignKey(
        Item,
        related_name="images",
        on_delete=models.CASCADE,
    )

    def get_image_x1280(self):
        return get_thumbnail(self.image, "1280", quality=51)

    def get_image_400x300(self):
        return get_thumbnail(self.image, "400x300", crop="center", quality=51)

    def image_tmb(self):
        if self.image:
            return mark_safe(
                f"img src='{self.image.url} width='50'",
            )
        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True
