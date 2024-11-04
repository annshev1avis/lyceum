import datetime
import random

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from tinymce.models import HTMLField

import catalog.validators
import core.models

__all__ = ["Category", "GalleryImage", "Item", "MainImage", "Tag"]


class ItemBusinessLogicManager(models.Manager):
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

    def on_main(self):
        return (
            self.published()
            .filter(is_on_main=True)
            .order_by("name")  # clear previous ordering
        )

    def new(self, amount):
        # возвращает случайные товары (в количестве amount),
        # которые были добавлены
        # за последнюю неделю (строго 24*7 часов с момента добавления в базу)

        convinient_ids = list(
            self.published()
            .filter(
                create_date__date__gt=(
                    datetime.datetime.now() - datetime.timedelta(days=7),
                ),
            )
            .values_list("id", flat=True),
        )
        random.shuffle(convinient_ids)

        if convinient_ids:
            will_show_ids = convinient_ids[: min(len(convinient_ids), 5)]
        else:
            will_show_ids = []

        return self.published().filter(id__in=will_show_ids)

    def friday(self):
        return (
            self.published()
            .filter(update_date__week_day=6)
            .order_by("-update_date")[:5]
        )

    def unverified(self):
        return self.published().filter(create_date=models.F("update_date"))


class Item(core.models.CoreModel):
    business_logic = ItemBusinessLogicManager()

    text = HTMLField(
        "текст",
        validators=[
            catalog.validators.ValidateMustContain("превосходно", "роскошно"),
        ],
        help_text="Опишите товар",
    )
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
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
