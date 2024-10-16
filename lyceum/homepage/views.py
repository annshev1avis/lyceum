import http

import django.http


def home(request):
    return django.http.HttpResponse("Главная")


def teapot(request):
    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )
