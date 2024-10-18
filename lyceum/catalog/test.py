import django.core.exceptions
import django.test

import catalog.models
from catalog.validators import ValidateMustContain


class CatalogTests(django.test.TestCase):
    def test_item_list(self):
        response = django.test.Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_item_detail_positive_int(self):
        response = django.test.Client().get("/catalog/4/")
        self.assertEqual(response.status_code, 200)

    def test_item_detail_negative_int(self):
        response = django.test.Client().get("/catalog/-1/")
        self.assertEqual(response.status_code, 404)

    def test_item_detail_big_int(self):
        response = django.test.Client().get("/catalog/1931/")
        self.assertEqual(response.status_code, 200)

    def test_item_detail_zero(self):
        response = django.test.Client().get("/catalog/0/")
        self.assertEqual(response.status_code, 200)

    def test_regex_positive_int(self):
        response = django.test.Client().get("/catalog/re/146/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_regex_negative_int(self):
        response = django.test.Client().get("/catalog/re/-146/")
        self.assertEqual(response.status_code, 404)

    def test_regex_zero(self):
        response = django.test.Client().get("/catalog/re/0/")
        self.assertEqual(response.status_code, 404)

    def test_regex_positive_int_with_leading_zeros(self):
        response = django.test.Client().get("/catalog/re/0000146/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_regex_float(self):
        response = django.test.Client().get("/catalog/re/146.0/")
        self.assertEqual(response.status_code, 404)

    def test_positive_int_converter_positive_int(self):
        response = django.test.Client().get("/catalog/converter/146/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_positive_int_converter_negative_int(self):
        response = django.test.Client().get("/catalog/converter/-146/")
        self.assertEqual(response.status_code, 404)

    def test_positive_int_converter_zero(self):
        response = django.test.Client().get("/catalog/converter/0/")
        self.assertEqual(response.status_code, 404)

    def test_positive_int_converter_positive_int_with_leading_zeros(self):
        response = django.test.Client().get("/catalog/converter/0000146/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_positive_int_converter_float(self):
        response = django.test.Client().get("/catalog/converter/146.0/")
        self.assertEqual(response.status_code, 404)


class ModelsTests(django.test.TestCase):
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
        with self.assertRaises(django.core.exceptions.ValidationError):
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

        with self.assertRaises(django.core.exceptions.ValidationError):
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


class ValidateMustContainTests(django.test.TestCase):
    def setUp(self):
        self.validator = ValidateMustContain("превосходно", "роскошно")

    def test_positive_1(self):
        self.assertEqual(
            self.validator("превосходно"),
            None,
        )

    def test_positive_2(self):
        self.assertEqual(
            self.validator("роскошно"),
            None,
        )

    def test_positive_with_punctuation(self):
        self.assertEqual(
            self.validator("(роскошно!)..."),
            None,
        )

    def test_positive_several_words(self):
        self.assertEqual(
            self.validator(
                "роскошно написанная книга",
            ),
            None,
        )

    def test_negative_unfinished_word(self):
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.validator("превосходн")

    def test_negative_several_words(self):
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.validator("обычно написанная книга")

    def test_negative_with_punctuation_but_not_word(self):
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.validator("лишнее(роскошно!)...")

    def test_negative_empty_string(self):
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.validator("")

    def test_negative_includes_word_substring_but_not_word(self):
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.validator("нероскошно")
