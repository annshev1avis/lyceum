from django.db import models


__all__ = []


class Feedback(models.Model):
    name = models.CharField(
        "Название",
        max_length=100,
        null=True,
        blank=True,
        help_text="О чем ваш фидбек",
    )
    text = models.TextField(
        "Текст фидбека",
        help_text="Поделитесь впечатлениями",
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
    )
    mail = models.EmailField(
        "Электронная почта",
        help_text="Введите электронную почту",
    )
