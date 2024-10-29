from django.test import Client, TestCase
from django.urls import reverse

import catalog.models

__all__ = []


class CatalogViewsTest(TestCase):
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

    def test_item_list(self):
        response = Client().get(reverse("catalog:item_list"))
        goods = response.context["goods"]
        self.assertEqual(
            len(goods),
            2,
            "Неправильное количество товаров в списке товаров",
        )

    def test_single_item(self):
        published_item_id = self.item1.id
        response = Client().get(
            reverse("catalog:item_detail", args=[published_item_id]),
        )
        self.assertIn("good", response.context)
        self.assertIn(
            "_prefetched_objects_cache",
            response.context["good"].__dict__,
            "Не загружаются связанные поля",
        )
        self.assertIsInstance(response.context["good"], catalog.models.Item)

    def test_single_item_unpublished(self):
        unpublished_item_id = self.item3_unpublished.id
        response = Client().get(
            reverse("catalog:item_detail", args=[unpublished_item_id]),
        )
        self.assertEqual(response.status_code, 404)