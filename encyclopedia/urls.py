from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('create/', views.create, name="create"),
    path('wiki/<str:pagetitle>', views.page, name="page"),
]