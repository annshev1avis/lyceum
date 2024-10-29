import http

from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render

import catalog.models


__all__ = ["home", "teapot"]


def home(request):
    template = "homepage/main.html"
    context = {
        "goods": (
            catalog.models.Item.active.filter(is_on_main=True)
            .select_related("category")
            .prefetch_related(
                Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.active.all().only("name"),
                ),
            )
            .order_by("name")
            .only("name", "category__name", "text", "tags")
        ),
    }
    return render(request, template, context)


def teapot(request):
    return HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )
