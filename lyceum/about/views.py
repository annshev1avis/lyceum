import django.http


def description(request):
    return django.http.HttpResponse("О проекте")
