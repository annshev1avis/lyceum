from django.urls import path

import homepage.views


app_name = "homepage"

urlpatterns = [
    path("", homepage.views.home, name="homepage"),
    path("coffee/", homepage.views.teapot, name="coffee"),
    path("echo/", homepage.views.echo_form, name="echo_form"),
    path("echo/submit/", homepage.views.echo_submit, name="echo_submit"),
]
