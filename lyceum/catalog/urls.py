import django.urls

import catalog.converters
import catalog.views

django.urls.register_converter(catalog.converters.PositiveInt, "positive_int")

urlpatterns = [
    django.urls.path("", catalog.views.item_list),
    django.urls.path("<int:detail>/", catalog.views.item_detail),
    django.urls.re_path(r"re/(0*[1-9][0-9]*)/", catalog.views.echo_num),
    django.urls.path("converter/<positive_int:num>/", catalog.views.echo_num),
]
