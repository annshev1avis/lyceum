from django.test import Client, TestCase


class CatalogTests(TestCase):
    def test_item_list(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "Список элементов")

    def test_item_detail_positive_int(self):
        response = Client().get("/catalog/4/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "Подробно элемент")

    def test_item_detail_negative_int(self):
        response = Client().get("/catalog/-1/")
        self.assertEqual(response.status_code, 404)

    def test_item_detail_big_int(self):
        response = Client().get("/catalog/1931/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "Подробно элемент")

    def test_item_detail_zero(self):
        response = Client().get("/catalog/0/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "Подробно элемент")

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
        self.assertEqual(response.status_code, 404)

    def test_regex_float(self):
        response = Client().get("/catalog/re/146.0/")
        self.assertEqual(response.status_code, 404)

    def test_month_converter_12(self):
        response = Client().get("/catalog/12/146/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_month_converter_8(self):
        response = Client().get("/catalog/8/146/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_month_converter_08(self):
        response = Client().get("/catalog/08/146/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_month_converter_15(self):
        response = Client().get("/catalog/15/146/")
        self.assertEqual(response.status_code, 404)
