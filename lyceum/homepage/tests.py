from django.test import Client, TestCase


class HomepageTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)
        str_content = str(response.content, encoding="utf-8")
        self.assertEqual(str_content, "Главная")
