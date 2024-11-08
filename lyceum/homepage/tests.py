import http

import django.test
from django.urls import reverse
from parameterized import parameterized

import catalog.models

__all__ = ["HomepageTests"]


class HomepageTests(django.test.TestCase):
    def setUp(self):
        self.category1 = catalog.models.Category(
            name="test_category_1",
            slug="category_1",
        )
        self.category1.save()

        self.item1 = catalog.models.Item(
            name="test_name_1",
            text="роскошно",
            is_published=True,
            is_on_main=True,
        )
        self.item2 = catalog.models.Item(
            name="test_name_2",
            text="роскошно",
            is_published=True,
        )
        self.item3_unpublished = catalog.models.Item(
            name="test_name_3",
            text="роскошно",
            is_published=False,
        )

        self.item1.category = self.category1
        self.item2.category = self.category1
        self.item3_unpublished.category = self.category1

        self.item1.save()
        self.item2.save()
        self.item3_unpublished.save()

        self.tag1 = catalog.models.Tag(name="test_tag_1", slug="tag_1")
        self.tag2 = catalog.models.Tag(name="test_tag_2", slug="tag_2")
        self.tag1.save()
        self.tag2.save()

        self.item1.tags.add(self.tag1)
        self.item1.tags.add(self.tag2)
        self.item2.tags.add(self.tag1)

        self.item1.save()
        self.item2.save()
        self.item3_unpublished.save()

    def test_homepage_items_in_context(self):
        response = django.test.Client().get(reverse("homepage:homepage"))
        self.assertIn("items", response.context)

    def test_homepage_items_len(self):
        response = django.test.Client().get(reverse("homepage:homepage"))
        self.assertEqual(len(response.context["items"]), 1)

    def test_homepage_items_type(self):
        response = django.test.Client().get(reverse("homepage:homepage"))
        for item in response.context["items"]:
            self.assertIsInstance(item, catalog.models.Item)

    @parameterized.expand(
        [
            ("is_published",),
            ("is_on_main",),
            ("main_image_id",),
        ],
    )
    def test_homepage_excludes_field_from_item(self, field):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            self.assertNotIn(field, item.__dict__)

    def test_homepage_excludes_images_from_item_prefetch(self):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            self.assertNotIn(
                "images",
                item.__dict__["_prefetched_objects_cache"],
            )

    @parameterized.expand(
        [
            ("is_published",),
            ("slug",),
            ("weight",),
        ],
    )
    def test_homepage_excludes_field_from_category(self, field):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            self.assertNotIn(field, item.category.__dict__)

    @parameterized.expand(
        [
            ("is_published",),
            ("slug",),
        ],
    )
    def test_homepage_excludes_field_from_tags(self, field):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            for tag in item.tags.all():
                self.assertNotIn(field, tag.__dict__)


class TeapotTests(django.test.TestCase):
    def test_teapot(self):
        responses_content = []

        for _ in range(2):
            response = django.test.Client().get(reverse("homepage:coffee"))
            self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)
            responses_content.append(str(response.content, encoding="utf-8"))

        self.assertIn("Я чайник", responses_content)


class EchoTests(django.test.TestCase):
    def test_form_in_context(self):
        response = django.test.Client().get(reverse("homepage:echo_form"))
        self.assertIn("form", response.context)

    def test_echo_post_is_unavailable(self):
        response = django.test.Client().post(reverse("homepage:echo_form"))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.METHOD_NOT_ALLOWED,
        )

    def test_submit_returns_plain_text(self):
        form_data = {"text": "sample_text"}
        response = django.test.Client().post(
            reverse("homepage:echo_submit"),
            form_data,
        )
        self.assertEqual(
            "text/plain; charset=utf-8",
            response.headers["Content-Type"],
        )

    def test_submit_returns_same_text(self):
        sample_text = "sample_text"

        form_data = {"text": sample_text}
        response = django.test.Client().post(
            reverse("homepage:echo_submit"),
            form_data,
        )
        self.assertEqual(sample_text.encode(), response.content)

    def test_submit_get_is_unavailable(self):
        response = django.test.Client().get(reverse("homepage:echo_submit"))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.METHOD_NOT_ALLOWED,
        )
