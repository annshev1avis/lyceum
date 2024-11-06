import datetime
from unittest import mock

from django.test import Client, TestCase
from django.urls import reverse
from parameterized import parameterized

import catalog.models

__all__ = []


class CatalogItemListTest(TestCase):
    def setUp(self):
        self.category1 = catalog.models.Category(
            name="test_category_1",
            slug="category_1",
        )
        self.category2 = catalog.models.Category(
            name="test_category_2",
            slug="category_2",
            is_published=False,
        )
        self.category1.save()
        self.category2.save()

        self.item1 = catalog.models.Item(
            name="test_name_1",
            text="роскошно",
            is_published=True,
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
        self.item4 = catalog.models.Item(
            name="test_name_4",
            text="роскошно",
            is_published=True,
        )

        self.item1.category = self.category1
        self.item2.category = self.category1
        self.item3_unpublished.category = self.category1
        self.item4.category = self.category2

        self.item1.save()
        self.item2.save()
        self.item3_unpublished.save()
        self.item4.save()

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
        self.item4.save()

    def test_item_list_items_in_context(self):
        response = Client().get(reverse("catalog:item_list"))
        self.assertIn("items", response.context)

    def test_item_list_items_len(self):
        response = Client().get(reverse("catalog:item_list"))
        self.assertEqual(len(response.context["items"]), 2)

    def test_item_list_items_type(self):
        response = Client().get(reverse("catalog:item_list"))
        for item in response.context["items"]:
            self.assertIsInstance(item, catalog.models.Item)

    def test_item_list_excludes_is_on_main(self):
        response = Client().get(reverse("catalog:item_list"))

        for item in response.context["items"]:
            self.assertNotIn("is_on_main", item.__dict__)

    def test_item_list_excludes_is_published(self):
        response = Client().get(reverse("catalog:item_list"))

        for item in response.context["items"]:
            self.assertNotIn("is_published", item.__dict__)

    def test_item_list_excludes_main_image(self):
        response = Client().get(reverse("catalog:item_list"))

        for item in response.context["items"]:
            self.assertNotIn("main_image_id", item.__dict__)

    def test_item_list_excludes_images(self):
        response = Client().get(reverse("catalog:item_list"))

        for item in response.context["items"]:
            self.assertNotIn(
                "images",
                item.__dict__["_prefetched_objects_cache"],
            )

    def test_item_list_excludes_category_is_published(self):
        response = Client().get(reverse("catalog:item_list"))

        for item in response.context["items"]:
            self.assertNotIn("is_published", item.category.__dict__)

    def test_item_list_excludes_category_weight(self):
        response = Client().get(reverse("catalog:item_list"))

        for item in response.context["items"]:
            self.assertNotIn("weight", item.category.__dict__)

    def test_item_list_excludes_category_slug(self):
        response = Client().get(reverse("catalog:item_list"))

        for item in response.context["items"]:
            self.assertNotIn("slug", item.category.__dict__)

    def test_item_list_excludes_tag_is_published(self):
        response = Client().get(reverse("catalog:item_list"))

        for item in response.context["items"]:
            for tag in item.tags.all():
                self.assertNotIn("is_published", tag.__dict__)

    def test_item_list_excludes_tag_slug(self):
        response = Client().get(reverse("catalog:item_list"))

        for item in response.context["items"]:
            for tag in item.tags.all():
                self.assertNotIn("slug", tag.__dict__)


class SingleItemTest(TestCase):
    def setUp(self):
        self.category1 = catalog.models.Category(
            name="test_category_1",
            slug="category_1",
        )
        self.category2 = catalog.models.Category(
            name="test_category_2",
            slug="category_2",
            is_published=False,
        )
        self.category1.save()
        self.category2.save()

        self.item1 = catalog.models.Item(
            name="test_name_1",
            text="роскошно",
            is_published=True,
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
        self.item4 = catalog.models.Item(
            name="test_name_4",
            text="роскошно",
            is_published=True,
        )

        self.item1.category = self.category1
        self.item2.category = self.category1
        self.item3_unpublished.category = self.category1
        self.item4.category = self.category2

        self.item1.save()
        self.item2.save()
        self.item3_unpublished.save()
        self.item4.save()

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
        self.item4.save()

    def test_single_item_item_in_context(self):
        published_item_id = self.item1.id
        response = Client().get(
            reverse("catalog:item_detail", args=[published_item_id]),
        )
        self.assertIn("item", response.context)

    def test_single_item_is_item_instance(self):
        published_item_id = self.item1.id
        response = Client().get(
            reverse("catalog:item_detail", args=[published_item_id]),
        )
        self.assertIsInstance(response.context["item"], catalog.models.Item)

    def test_single_item_excludes_is_on_main(self):
        published_item_id = self.item1.id
        response = Client().get(
            reverse("catalog:item_detail", args=[published_item_id]),
        )

        item = response.context["item"]
        self.assertNotIn("is_on_main", item.__dict__)

    def test_single_item_excludes_is_published(self):
        published_item_id = self.item1.id
        response = Client().get(
            reverse("catalog:item_detail", args=[published_item_id]),
        )

        item = response.context["item"]
        self.assertNotIn("is_published", item.__dict__)

    def test_single_item_excludes_category_is_published(self):
        published_item_id = self.item1.id
        response = Client().get(
            reverse("catalog:item_detail", args=[published_item_id]),
        )
        item = response.context["item"]

        self.assertNotIn("is_published", item.category.__dict__)

    def test_single_item_excludes_category_weight(self):
        published_item_id = self.item1.id
        response = Client().get(
            reverse("catalog:item_detail", args=[published_item_id]),
        )
        item = response.context["item"]

        self.assertNotIn("weight", item.category.__dict__)

    def test_single_item_excludes_category_slug(self):
        published_item_id = self.item1.id
        response = Client().get(
            reverse("catalog:item_detail", args=[published_item_id]),
        )
        item = response.context["item"]

        self.assertNotIn("slug", item.category.__dict__)

    def test_single_item_excludes_tag_is_published(self):
        published_item_id = self.item1.id
        response = Client().get(
            reverse("catalog:item_detail", args=[published_item_id]),
        )
        item = response.context["item"]

        for tag in item.tags.all():
            self.assertNotIn("is_published", tag.__dict__)

    def test_single_item_excludes_tag_slug(self):
        published_item_id = self.item1.id
        response = Client().get(
            reverse("catalog:item_detail", args=[published_item_id]),
        )
        item = response.context["item"]

        for tag in item.tags.all():
            self.assertNotIn("slug", tag.__dict__)


class NewFridayUnverifiedItemListTest(TestCase):
    def setUp(self):
        self.test_category = catalog.models.Category(
            name="test_category_1",
            slug="category_1",
        )
        self.test_category.save()

        self.create_item_on_friday()
        self.create_item_2024_11_06()

    @mock.patch(
        "django.utils.timezone.now",
        mock.Mock(
            return_value=datetime.datetime(
                2024,
                10,
                25,
                tzinfo=datetime.timezone.utc,
            ),
        ),
    )
    def create_item_on_friday(self):
        self.item_friday = catalog.models.Item(
            name="test item friday",
            text="роскошно",
            category=self.test_category,
        )
        self.item_friday.save()

    @mock.patch(
        "django.utils.timezone.now",
        mock.Mock(
            return_value=datetime.datetime(
                2024,
                11,
                6,
                tzinfo=datetime.timezone.utc,
            ),
        ),
    )
    def create_item_2024_11_06(self):
        self.item_2024_11_06 = catalog.models.Item(
            name="test item new",
            text="роскошно",
            category=self.test_category,
        )
        self.item_2024_11_06.save()

    @parameterized.expand(
        [
            ("catalog:item_list_new",),
            ("catalog:item_list_friday",),
            ("catalog:item_list_unverified",),
        ],
    )
    def test_status_code(self, url_name):
        response = Client().get(reverse(url_name))
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("catalog:item_list_new",),
            ("catalog:item_list_friday",),
            ("catalog:item_list_unverified",),
        ],
    )
    def test_items_in_context(self, url_name):
        response = Client().get(reverse(url_name))
        self.assertIn("items", response.context)

    @mock.patch(
        "django.utils.timezone.now",
        mock.Mock(
            return_value=datetime.datetime(
                2024,
                11,
                7,
                tzinfo=datetime.timezone.utc,
            ),
        ),
    )
    def test_new_len(self):
        response = Client().get(reverse("catalog:item_list_new"))
        items = response.context["items"]
        self.assertEqual(len(items), 1)

    def test_friday_len(self):
        response = Client().get(reverse("catalog:item_list_friday"))
        items = response.context["items"]
        self.assertEqual(len(items), 1)

    def test_unverified_len(self):
        response = Client().get(reverse("catalog:item_list_unverified"))
        items = response.context["items"]
        self.assertEqual(len(items), 2)
