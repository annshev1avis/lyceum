from django.db.models import Prefetch
import django.http
from django.shortcuts import get_object_or_404, render

import catalog.models

__all__ = ["echo_num", "item_detail", "item_list"]


def item_list(request):
    template = "catalog/item_list.html"
    context = {
        "title": "Каталог",
        "items": catalog.models.Item.business_logic.published(),
    }
    return render(request, template, context)


def item_list_new_5(request):
    template = "catalog/item_list.html"
    context = {
        "title": "Новинки",
        "items": catalog.models.Item.business_logic.new(5),
    }
    return render(request, template, context)


def item_list_friday(request):
    template = "catalog/item_list.html"
    context = {
        "title": "Пятница",
        "items": catalog.models.Item.business_logic.friday(),
    }
    return render(request, template, context)


def item_list_unverified(request):
    template = "catalog/item_list.html"
    context = {
        "title": "Непроверенное",
        "items": catalog.models.Item.business_logic.unverified(),
    }
    return render(request, template, context)


def item_detail(request, detail):
    template = "catalog/item.html"
    context = {
        "item": get_object_or_404(
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
