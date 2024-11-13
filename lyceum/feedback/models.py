import time

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
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        help_text="Текущий этап обработки фидбека",
    )
    text = models.TextField(
        "Текст фидбека",
        help_text="Поделитесь впечатлениями",
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.text if len(self.text) < 35 else f"{self.text[:35]}..."

    class Meta:
        verbose_name = "фидбек"
        verbose_name_plural = "фидбеки"


class FeedbackAuthor(models.Model):
    name = models.CharField(
        "Имя",
        max_length=100,
        null=True,
        blank=True,
        help_text="Введите ваше имя",
    )
    mail = models.EmailField(
        "Электронная почта",
        help_text="Введите электронную почту",
    )
    feedback = models.OneToOneField(
        Feedback,
        on_delete=models.CASCADE,
        related_name="author",
    )

    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "авторы"


class FeedbackFile(models.Model):
    def get_path(self, filename):
        return f"uploads/{12}/{time.time()}_{filename}"

    file = models.FileField(
        "Файл",
        upload_to=get_path,
        blank=True,
    )
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name="files",
    )

    class Meta:
        verbose_name = "файл"
        verbose_name_plural = "файлы"
