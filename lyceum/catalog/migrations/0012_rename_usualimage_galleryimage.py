# Generated by Django 4.2.16 on 2024-10-25 11:29

from django.db import migrations

__all__ = ["Migration"]


class Migration(migrations.Migration):

    dependencies = [
        (
            "catalog",
            "0011_mainimage_usualimage_remove_item_main_image_and_more",
        ),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UsualImage",
            new_name="GalleryImage",
        ),
    ]
