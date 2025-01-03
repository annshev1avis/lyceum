# Generated by Django 4.2.16 on 2024-11-06 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("catalog", "0020_alter_item_create_date_alter_item_update_date"),
        (
            "catalog",
            "0021_remove_item_create_date_remove_item_update_date_and_more",
        ),
        (
            "catalog",
            "0022_category_canonical_name_item_canonical_name_and_more",
        ),
    ]

    dependencies = [
        ("catalog", "0019_item_create_date_item_update_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="item",
            name="create_date",
        ),
        migrations.RemoveField(
            model_name="item",
            name="update_date",
        ),
        migrations.AddField(
            model_name="item",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="время создания"
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="updated",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="время обновления"
            ),
        ),
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
