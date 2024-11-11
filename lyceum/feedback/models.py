from django.conf import settings
from django.db import models


__all__ = []


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    status_from = models.CharField(
        max_length=20,
        db_column="from",
    )
    status_to = models.CharField(
        max_length=20,
        db_column="to",
    )


class Feedback(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Получено"
        WIP = "wip", "В обработке"
        ANS = "ans", "Ответ дан"

    status = models.CharField(
        "статус",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        help_text="Текущий этап обработки фидбека",
    )
    name = models.CharField(
        "Имя",
        max_length=100,
        null=True,
        blank=True,
        help_text="Введите ваше имя",
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

    def __str__(self):
        return self.text if len(self.text) < 35 else f"{self.text[:35]}..."

    class Meta:
        verbose_name = "фидбек"
        verbose_name_plural = "фидбеки"
