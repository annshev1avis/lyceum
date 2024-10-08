from django.contrib import admin
from django.urls import include, path

from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("about/", include("about.urls")),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
