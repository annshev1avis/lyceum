# Generated by Django 4.2.16 on 2024-10-30 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0016_alter_item_managers_alter_item_is_on_main"),
    ]

    operations = [
        migrations.AlterField(
            model_name="galleryimage",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                related_query_name="images",
                to="catalog.item",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.ForeignKey(
                help_text="Выберите категорию",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                related_query_name="items",
                to="catalog.category",
                verbose_name="категория",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="tags",
            field=models.ManyToManyField(
                help_text="Можно выбрать несколько тегов",
                related_name="items",
                related_query_name="items",
                to="catalog.tag",
                verbose_name="теги",
            ),
        ),
        migrations.AlterField(
            model_name="mainimage",
            name="item",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="main_image",
                related_query_name="main_image",
                to="catalog.item",
            ),
        ),
    ]
