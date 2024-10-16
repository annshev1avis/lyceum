import django.http


def item_list(request):
    return django.http.HttpResponse("Список элементов")


def item_detail(request, detail):
    return django.http.HttpResponse("Подробно элемент")


def echo_num(request, num):
    num = int(num)
    return django.http.HttpResponse(str(num))
