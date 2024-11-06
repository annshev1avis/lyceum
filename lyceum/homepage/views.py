import http

from django.http import HttpResponse
from django.shortcuts import render

import catalog.models


__all__ = ["home", "teapot"]


def home(request):
    template = "homepage/main.html"
    context = {
        "title": "Главная",
        "items": catalog.models.Item.business_logic.on_main(),
    }
    return render(request, template, context)


def teapot(request):
    return HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )
