from django.urls import path

import download.views

app_name = "download"

urlpatterns = [
    path(
        "<path:path>/",
        download.views.download_media_file,
        name="download_media_file",
    ),
]
