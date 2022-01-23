from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("wiki/<str:title>", views.article, name="article"),
    path("random/", views.randompage, name="randompage"),
    path("search/", views.search_page, name="search")
]
