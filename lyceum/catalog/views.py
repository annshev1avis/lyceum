import django.http
from django.shortcuts import render

__all__ = ["echo_num", "item_detail", "item_list"]


def item_list(request):
    template = "catalog/item_list.html"
    context = {
        "goods": [
            {"name": "енот 1", "description": "добрый"},
            {"name": "енот 2", "description": "дружелюбный"},
            {"name": "енот 3", "description": "грустный"},
        ],
    }
    return render(request, template, context)


def item_detail(request, detail):
    template = "catalog/item.html"
    context = {"name": f"енот {detail}"}
    return render(request, template, context)


def echo_num(request, num):
    num = int(num)
    return django.http.HttpResponse(str(num))
