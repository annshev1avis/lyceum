import django.core.exceptions
import django.db.models

import catalog.validators
import core.models


class Item(core.models.CoreModel):
    text = django.db.models.TextField(
        "текст",
        validators=[
            catalog.validators.ValidateMustContain("превосходно", "роскошно"),
        ],
        help_text="Опишите товар",
    )
    category = django.db.models.ForeignKey(
        "Category",
        on_delete=django.db.models.CASCADE,
        related_name="items",
        verbose_name="категория",
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        "Tag",
        related_name="items",
        verbose_name="теги",
        help_text="Можно выбрать несколько тегов",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return f"{self.name}"


class Tag(core.models.CoreModel):
    slug = django.db.models.SlugField(
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
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="Слаг может состоять из латинских букв, "
        "цифр и нижнего подчеркивания",
    )

    weight = django.db.models.IntegerField(
        "вес",
        default=100,
        validators=[catalog.validators.is_int_1_32767],
        help_text="Введите число от 1 до 32767",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return f"{self.name}"
