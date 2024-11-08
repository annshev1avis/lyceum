import http

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render

import catalog.models
import homepage.forms


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


def echo_form(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    context = {"form": homepage.forms.EchoForm()}
    return render(request, "homepage/echo_form.html", context)


def echo_submit(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    return HttpResponse(
        request.POST["text"],
        content_type="text/plain; charset=utf-8",
    )
