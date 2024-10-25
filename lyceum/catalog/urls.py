import django.urls

import catalog.converters
import catalog.views

django.urls.register_converter(catalog.converters.PositiveInt, "positive_int")

app_name = "catalog"

urlpatterns = [
    django.urls.path("", catalog.views.item_list, name="item_list"),
    django.urls.path(
        "<int:detail>/",
        catalog.views.item_detail,
        name="item_detail",
    ),
    django.urls.re_path(
        r"re/(0*[1-9][0-9]*)/",
        catalog.views.echo_num,
        name="item_detail_re",
    ),
    django.urls.path(
        "converter/<positive_int:num>/",
        catalog.views.echo_num,
        name="item_detail_positive_convert",
    ),
]
