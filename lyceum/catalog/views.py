from django.http import HttpResponse


def item_list(request):
    return HttpResponse("Список элементов")


def item_detail(request, detail):
    return HttpResponse("Подробно элемент")


def echo_num(request, num):
    return HttpResponse(str(num))


def month_and_num(request, month, num):
    return HttpResponse(str(num))
