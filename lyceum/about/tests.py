import django.test

__all__ = ["AboutTests"]


class AboutTests(django.test.TestCase):
    def test_about(self):
        response = django.test.Client().get("/about/")
        self.assertEqual(response.status_code, 200)
