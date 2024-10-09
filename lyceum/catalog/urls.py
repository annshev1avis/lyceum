from django.urls import path, re_path, register_converter

from . import converters, views

register_converter(converters.MonthConverter, "month_num")

urlpatterns = [
    path("", views.item_list),
    path("<int:detail>/", views.item_detail),
    re_path(r"re/([1-9][0-9]*)/", views.echo_num),
    path("<month_num:month>/<int:num>/", views.month_and_num),
]
