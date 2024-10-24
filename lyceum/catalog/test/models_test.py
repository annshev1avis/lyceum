from django.core.exceptions import ValidationError
from django.test import TestCase

import catalog.models


class ModelsTests(TestCase):
    fixtures = ["fixtures/data.json"]

    def test_creating_tag(self):
        initial_amount = catalog.models.Tag.objects.count()
        tag = catalog.models.Tag(name="Тестовый тег", slug="test_tag")
        tag.full_clean()
        tag.save()

        self.assertEqual(
            initial_amount + 1,
            catalog.models.Tag.objects.count(),
        )

    def test_creating_category(self):
        initial_amount = catalog.models.Category.objects.count()

        category = catalog.models.Category.objects.create(
            name="Тестовая категория",
            slug="test_category",
        )
        category.full_clean()
        category.save()

        self.assertEqual(
            initial_amount + 1,
            catalog.models.Category.objects.count(),
        )

    def test_creating_category_wrong_weight_validator(self):
        initial_amount = catalog.models.Category.objects.count()
        with self.assertRaises(ValidationError):
            category = catalog.models.Category(
                name="Тестовая категория",
                slug="test_category",
                weight=40000,
            )
            category.full_clean()
            category.save()

        self.assertEqual(
            initial_amount,
            catalog.models.Category.objects.count(),
        )

    def test_creating_item(self):
        initial_amount = catalog.models.Item.objects.count()

        test_category = catalog.models.Category.objects.all()[0]
        test_tag1 = catalog.models.Tag.objects.all()[0]
        test_tag2 = catalog.models.Tag.objects.all()[0]

        item = catalog.models.Item(
            name="Кулинария для джангистов",
            text="Роскошно",
            category=test_category,
        )
        item.full_clean()
        item.save()
        item.tags.add(test_tag1)
        item.tags.add(test_tag2)
        item.full_clean()
        item.save()

        self.assertEqual(
            initial_amount + 1,
            catalog.models.Item.objects.count(),
        )

    def test_creating_item_wrong_text_validator(self):
        initial_amount = catalog.models.Item.objects.count()

        test_category = catalog.models.Category.objects.all()[0]
        test_tag1 = catalog.models.Tag.objects.all()[0]
        test_tag2 = catalog.models.Tag.objects.all()[0]

        with self.assertRaises(ValidationError):
            item = catalog.models.Item(
                name="Кулинария для джангистов",
                text="нет нужного слова",
                category=test_category,
            )
            item.full_clean()
            item.save()
            item.tags.add(test_tag1)
            item.tags.add(test_tag2)
            item.full_clean()
            item.save()

        self.assertEqual(initial_amount, catalog.models.Item.objects.count())
