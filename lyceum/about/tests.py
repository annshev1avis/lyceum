import django.test
from django.urls import reverse

__all__ = ["AboutTests"]


class AboutTests(django.test.TestCase):
    def test_about(self):
        response = django.test.Client().get(reverse("about:about"))
        self.assertEqual(response.status_code, 200)
