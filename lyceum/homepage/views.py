from django.http import HttpResponse


def home(request):
    return HttpResponse("Главная")


def teapot(request):
    return HttpResponse("Я чайник", status=418)
