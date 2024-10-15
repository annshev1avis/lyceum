from django.core.exceptions import ValidationError
from django.test import Client, TestCase

from . import models


class CatalogTests(TestCase):
    def test_item_list(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_item_detail_positive_int(self):
        response = Client().get("/catalog/4/")
        self.assertEqual(response.status_code, 200)

    def test_item_detail_negative_int(self):
        response = Client().get("/catalog/-1/")
        self.assertEqual(response.status_code, 404)

    def test_item_detail_big_int(self):
        response = Client().get("/catalog/1931/")
        self.assertEqual(response.status_code, 200)

    def test_item_detail_zero(self):
        response = Client().get("/catalog/0/")
        self.assertEqual(response.status_code, 200)

    def test_regex_positive_int(self):
        response = Client().get("/catalog/re/146/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_regex_negative_int(self):
        response = Client().get("/catalog/re/-146/")
        self.assertEqual(response.status_code, 404)

    def test_regex_zero(self):
        response = Client().get("/catalog/re/0/")
        self.assertEqual(response.status_code, 404)

    def test_regex_positive_int_with_leading_zeros(self):
        response = Client().get("/catalog/re/0000146/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_regex_float(self):
        response = Client().get("/catalog/re/146.0/")
        self.assertEqual(response.status_code, 404)

    def test_positive_int_converter_positive_int(self):
        response = Client().get("/catalog/converter/146/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_positive_int_converter_negative_int(self):
        response = Client().get("/catalog/converter/-146/")
        self.assertEqual(response.status_code, 404)

    def test_positive_int_converter_zero(self):
        response = Client().get("/catalog/converter/0/")
        self.assertEqual(response.status_code, 404)

    def test_positive_int_converter_positive_int_with_leading_zeros(self):
        response = Client().get("/catalog/converter/0000146/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_positive_int_converter_float(self):
        response = Client().get("/catalog/converter/146.0/")
        self.assertEqual(response.status_code, 404)


class ModelsTests(TestCase):
    fixtures = ["fixtures/data.json"]

    def test_creating_tag(self):
        initial_amount = models.Tag.objects.count()
        tag = models.Tag(name="Тестовый тег", slug="test_tag")
        tag.full_clean()
        tag.save()

        self.assertEqual(initial_amount + 1, models.Tag.objects.count())

    def test_creating_category(self):
        initial_amount = models.Category.objects.count()

        category = models.Category.objects.create(
            name="Тестовая категория", slug="test_category"
        )
        category.full_clean()
        category.save()

        self.assertEqual(initial_amount + 1, models.Category.objects.count())

    def test_creating_category_wrong_weight_validator(self):
        initial_amount = models.Category.objects.count()
        with self.assertRaises(ValidationError):
            category = models.Category(
                name="Тестовая категория", slug="test_category", weight=40000
            )
            category.full_clean()
            category.save()

        self.assertEqual(initial_amount, models.Category.objects.count())

    def test_creating_item(self):
        initial_amount = models.Item.objects.count()

        test_category = models.Category.objects.all()[0]
        test_tag1 = models.Tag.objects.all()[0]
        test_tag2 = models.Tag.objects.all()[0]

        item = models.Item(
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

        self.assertEqual(initial_amount + 1, models.Item.objects.count())

    def test_creating_item_wrong_text_validator(self):
        initial_amount = models.Item.objects.count()

        test_category = models.Category.objects.all()[0]
        test_tag1 = models.Tag.objects.all()[0]
        test_tag2 = models.Tag.objects.all()[0]

        with self.assertRaises(ValidationError):
            item = models.Item(
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

        self.assertEqual(initial_amount, models.Item.objects.count())
