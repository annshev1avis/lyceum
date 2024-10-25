import django.core.exceptions
import django.test
from django.urls import NoReverseMatch, reverse


__all__ = ["CatalogTests"]


class CatalogTests(django.test.TestCase):
    def test_item_list(self):
        response = django.test.Client().get(reverse("catalog:item_list"))
        self.assertEqual(response.status_code, 200)

    def test_item_detail_positive_int(self):
        response = django.test.Client().get(
            reverse("catalog:item_detail", args=[4]),
        )
        self.assertEqual(response.status_code, 200)

    def test_item_detail_negative_int(self):
        with self.assertRaises(NoReverseMatch):
            django.test.Client().get(
                reverse("catalog:item_detail", args=[-1]),
            )

    def test_item_detail_big_int(self):
        response = django.test.Client().get(
            reverse("catalog:item_detail", args=[1931]),
        )
        self.assertEqual(response.status_code, 200)

    def test_item_detail_zero(self):
        response = django.test.Client().get(
            reverse("catalog:item_detail", args=[0]),
        )
        self.assertEqual(response.status_code, 200)

    def test_regex_positive_int(self):
        response = django.test.Client().get(
            reverse("catalog:item_detail_re", args=[146]),
        )
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_regex_negative_int(self):
        with self.assertRaises(NoReverseMatch):
            django.test.Client().get(
                reverse("catalog:item_detail_re", args=[-146]),
            )

    def test_regex_zero(self):
        with self.assertRaises(NoReverseMatch):
            django.test.Client().get(
                reverse("catalog:item_detail_re", args=["0"]),
            )

    def test_regex_positive_int_with_leading_zeros(self):
        response = django.test.Client().get(
            reverse("catalog:item_detail_re", args=["0000146"]),
        )
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_regex_float(self):
        with self.assertRaises(NoReverseMatch):
            django.test.Client().get(
                reverse("catalog:item_detail_re", args=["146.0"]),
            )

    def test_positive_int_converter_positive_int(self):
        response = django.test.Client().get(
            reverse("catalog:item_detail_positive_convert", args=[146]),
        )
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_positive_int_converter_negative_int(self):
        with self.assertRaises(NoReverseMatch):
            django.test.Client().get(
                reverse("catalog:item_detail_positive_convert", args=[-146]),
            )

    def test_positive_int_converter_zero(self):
        with self.assertRaises(NoReverseMatch):
            django.test.Client().get(
                reverse("catalog:item_detail_positive_convert", args=[0]),
            )

    def test_positive_int_converter_positive_int_with_leading_zeros(self):
        response = django.test.Client().get(
            reverse("catalog:item_detail_positive_convert", args=["0000146"]),
        )
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding="utf-8")
        self.assertEqual(content, "146")

    def test_positive_int_converter_float(self):
        with self.assertRaises(NoReverseMatch):
            django.test.Client().get(
                reverse(
                    "catalog:item_detail_positive_convert",
                    args=["146.0"],
                ),
            )
