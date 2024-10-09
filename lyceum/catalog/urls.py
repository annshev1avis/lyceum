from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.item_list),
    path("<int:detail>/", views.item_detail),
]
