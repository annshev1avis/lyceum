from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from tinymce.models import HTMLField

import catalog.validators
import core.models

__all__ = ["Category", "GalleryImage", "Item", "MainImage", "Tag"]


class ItemBusinessLogicManager(models.Manager):
    def on_main(self):
        return (
            self.get_queryset()
            .select_related("category")
            .filter(
                is_published=True,
                category__is_published=True,
                is_on_main=True,
            )
            .prefetch_related(
                models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.active.all().only("name"),
                ),
            )
            .order_by("name")
            .only("name", "category__name", "text", "tags")
        )

    def published(self):
        return (
            self.get_queryset()
            .select_related("category")
            .filter(is_published=True, category__is_published=True)
            .prefetch_related(
                models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.active.all().only("name"),
                ),
            )
            .order_by("category__name", "name")
            .only("name", "category__name", "text", "tags")
        )


class Item(core.models.CoreModel):
    business_logic = ItemBusinessLogicManager()

    text = HTMLField(
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
        related_query_name="items",
        verbose_name="категория",
        help_text="Выберите категорию",
    )
    tags = models.ManyToManyField(
        "Tag",
        related_name="items",
        related_query_name="items",
        verbose_name="теги",
        help_text="Можно выбрать несколько тегов",
    )
    is_on_main = models.BooleanField(
        "отображать на главной странице",
        default=False,
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ("name",)

    def __str__(self):
        return self.name


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


class MainImage(core.models.ImageModel):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name="main_image",
        related_query_name="main_image",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class GalleryImage(core.models.ImageModel):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="images",
        related_query_name="images",
    )

    class Meta:
        verbose_name = "обычное изображение"
        verbose_name_plural = "обычные изображения"
