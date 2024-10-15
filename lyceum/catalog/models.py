import django.db.models
from django.core.exceptions import ValidationError

import core.models


def is_int_1_32767(value):
    if not 1 <= value <= 32767:
        raise ValidationError("Число должно быть целым и принадлежать промежутку от 1 до 32767")


def contains_excellent_word(text):
    excellent_words = ("превосходно", "роскошно")

    text = text.lower()
    for word in excellent_words:
        if word in text:
            return

    raise ValidationError("Текст должен содеражать слово 'превосходно' или 'роскошно'")


class Item(core.models.CoreModel):
    text = django.db.models.TextField("Текст", validators=[contains_excellent_word])
    category = django.db.models.ForeignKey("Category", on_delete=django.db.models.PROTECT, related_name="items", verbose_name="Категория")
    tags = django.db.models.ManyToManyField("Tag", related_name="items", verbose_name="Теги")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name}"


class Tag(core.models.CoreModel):
    slug = django.db.models.SlugField("Слаг", max_length=200, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return f"{self.name}"


class Category(core.models.CoreModel):
    slug = django.db.models.SlugField("Слаг", max_length=200, unique=True)
    weight = django.db.models.IntegerField("Вес", default=100, validators=[is_int_1_32767])

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"
