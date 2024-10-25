import django.core.exceptions
import django.test

__all__ = ["CatalogTests"]


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
