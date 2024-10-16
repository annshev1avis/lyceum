import django.test


class AboutTests(django.test.TestCase):
    def test_about(self):
        response = django.test.Client().get("/about/")
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "О проекте")
