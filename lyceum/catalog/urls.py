from django.urls import path, re_path, register_converter

from . import converters, views

register_converter(converters.PositiveInt, "positive_int")

urlpatterns = [
    path("", views.item_list),
    path("<int:detail>/", views.item_detail),
    re_path(r"re/(0*[1-9][0-9]*)/", views.echo_num),
    path("converter/<positive_int:num>/", views.echo_num),
]
