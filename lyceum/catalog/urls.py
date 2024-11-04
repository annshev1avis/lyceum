from django.urls import path, re_path, register_converter

import catalog.converters
import catalog.views

register_converter(catalog.converters.PositiveInt, "positive_int")

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.item_list, name="item_list"),
    path("new/", catalog.views.item_list_new_5, name="item_list_new"),
    path("friday/", catalog.views.item_list_friday, name="item_list_friday"),
    path(
        "unverified/",
        catalog.views.item_list_unverified,
        name="item_list_unverified",
    ),
    path(
        "<int:detail>/",
        catalog.views.item_detail,
        name="item_detail",
    ),
    re_path(
        r"re/(0*[1-9][0-9]*)/",
        catalog.views.echo_num,
        name="item_detail_re",
    ),
    path(
        "converter/<positive_int:num>/",
        catalog.views.echo_num,
        name="item_detail_positive_convert",
    ),
]
