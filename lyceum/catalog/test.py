from django.test import Client, TestCase


class CatalogTests(TestCase):
    def test_item_list(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "Список элементов")

    def test_item_detail(self):
        response = Client().get("/catalog/4")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "Подробно элемент")
