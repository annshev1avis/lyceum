import http

from django.http import HttpResponse
from django.shortcuts import render

__all__ = ["MyClass", "home", "teapot"]


class MyClass:
    def __str__(self):
        return "MyClass"


def home(request):
    template = "homepage/main.html"
    context = {
        "goods": [
            {"name": "енот 1", "description": "добрый"},
            {"name": "енот 2", "description": "дружелюбный"},
            {"name": "енот 3", "description": "грустный"},
        ],
    }
    return render(request, template, context)


def teapot(request):
    return HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )
