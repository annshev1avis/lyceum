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

    def test_homepage_endpoint(self):
        response = django.test.Client().get(reverse("homepage:homepage"))
        goods = response.context["goods"]
        self.assertEqual(len(goods), 1)

    def test_teapot_endpoint(self):
        responses_content = []

        for _ in range(2):
            response = django.test.Client().get(reverse("homepage:coffee"))
            self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)
            responses_content.append(str(response.content, encoding="utf-8"))

        self.assertIn("Я чайник", responses_content)
