# Generated by Django 4.2.16 on 2024-10-25 11:29

from django.db import migrations

__all__ = ["Migration"]


class Migration(migrations.Migration):

    dependencies = [
        (
            "catalog",
            "0001_squashed_0013_alter_category_id_alter_item_id_alter_tag_id",
        ),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UsualImage",
            new_name="GalleryImage",
        ),
    ]
