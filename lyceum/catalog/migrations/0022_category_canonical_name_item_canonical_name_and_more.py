# Generated by Django 4.2.16 on 2024-11-05 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "catalog",
            "0021_remove_item_create_date_remove_item_update_date_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="canonical_name",
            field=models.CharField(
                editable=False,
                help_text="Каноническое название элемента",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="каноническое название",
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="canonical_name",
            field=models.CharField(
                editable=False,
                help_text="Каноническое название элемента",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="каноническое название",
            ),
        ),
        migrations.AddField(
            model_name="tag",
            name="canonical_name",
            field=models.CharField(
                editable=False,
                help_text="Каноническое название элемента",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="каноническое название",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                help_text="Введите уникальное название",
                max_length=150,
                unique=True,
                verbose_name="название",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="name",
            field=models.CharField(
                help_text="Введите уникальное название",
                max_length=150,
                unique=True,
                verbose_name="название",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(
                help_text="Введите уникальное название",
                max_length=150,
                unique=True,
                verbose_name="название",
            ),
        ),
    ]
