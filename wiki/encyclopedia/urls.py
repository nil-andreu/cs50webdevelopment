from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="page"),
    path("new", views.new, name="new"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.random, name="random")  
]
