from django.test import Client, TestCase


class AboutTests(TestCase):
    def test_about(self):
        response = Client().get("/about/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "О проекте")
