# Generated by Django 4.2.16 on 2024-10-25 20:22

import catalog.validators
from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0013_alter_category_id_alter_item_id_alter_tag_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="text",
            field=tinymce.models.HTMLField(
                help_text="Опишите товар",
                validators=[
                    catalog.validators.ValidateMustContain(
                        "превосходно", "роскошно"
                    )
                ],
                verbose_name="текст",
            ),
        ),
    ]
