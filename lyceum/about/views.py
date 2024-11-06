from django.shortcuts import render

__all__ = ["description"]


def description(request):
    template = "about/about.html"
    context = {"title": "О проекте"}
    return render(request, template, context)
