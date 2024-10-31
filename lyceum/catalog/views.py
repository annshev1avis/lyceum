from django.db.models import Prefetch
import django.http
from django.shortcuts import get_object_or_404, render

import catalog.models

__all__ = ["echo_num", "item_detail", "item_list"]


def item_list(request):
    template = "catalog/item_list.html"
    context = {
        "goods": (
            catalog.models.Item.active.select_related("category")
            .filter(category__is_published=True)
            .prefetch_related(
                Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.active.all().only("name"),
                ),
            )
            .order_by("category__name", "name")
            .only("name", "category__name", "text", "tags")
        ),
    }
    return render(request, template, context)


def item_detail(request, detail):
    template = "catalog/item.html"
    context = {
        "good": get_object_or_404(
            (
                catalog.models.Item.active.filter(category__is_published=True)
                .select_related("category")
                .select_related("main_image")
                .prefetch_related("images")
                .prefetch_related(
                    Prefetch(
                        "tags",
                        queryset=catalog.models.Tag.active.all().only("name"),
                    ),
                )
                .only(
                    "name",
                    "category__name",
                    "text",
                    "tags",
                    "main_image",
                    "images",
                )
            ),
            pk=detail,
        ),
    }
    return render(request, template, context)


def echo_num(request, num):
    num = int(num)
    return django.http.HttpResponse(str(num))
