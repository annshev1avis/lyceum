import http

import django.test
from django.urls import reverse

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

    def test_homepage_excludes_is_on_main(self):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            self.assertNotIn("is_on_main", item.__dict__)

    def test_homepage_excludes_is_published(self):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            self.assertNotIn("is_published", item.__dict__)

    def test_homepage_excludes_main_image(self):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            self.assertNotIn("main_image_id", item.__dict__)

    def test_homepage_excludes_images(self):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            self.assertNotIn(
                "images",
                item.__dict__["_prefetched_objects_cache"],
            )

    def test_homepage_excludes_category_is_published(self):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            self.assertNotIn("is_published", item.category.__dict__)

    def test_homepage_excludes_category_weight(self):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            self.assertNotIn("weight", item.category.__dict__)

    def test_homepage_excludes_category_slug(self):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            self.assertNotIn("slug", item.category.__dict__)

    def test_homepage_excludes_tag_is_published(self):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            self.assertNotIn("slug", item.category.__dict__)

            for tag in item.tags.all():
                self.assertNotIn("is_published", tag.__dict__)

    def test_homepage_excludes_tag_slug(self):
        response = django.test.Client().get(reverse("homepage:homepage"))

        for item in response.context["items"]:
            self.assertNotIn("slug", item.category.__dict__)

            for tag in item.tags.all():
                self.assertNotIn("slug", tag.__dict__)


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

    def test_submit_returns_plain_text(self):
        form_data = {"text": "sample_text"}
        response = django.test.Client().post(
            reverse("homepage:echo_submit"),
            form_data,
        )
        self.assertEqual("text/plain", response.headers["Content-Type"])

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
