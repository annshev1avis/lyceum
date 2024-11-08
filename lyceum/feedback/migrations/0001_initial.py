# Generated by Django 4.2.16 on 2024-11-08 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="О чем ваш фидбек",
                        max_length=100,
                        verbose_name="Название",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Поделитесь впечатлениями",
                        verbose_name="Текст фидбека",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "mail",
                    models.EmailField(
                        help_text="Введите электронную почту",
                        max_length=254,
                        verbose_name="Электронная почта",
                    ),
                ),
            ],
        ),
    ]
