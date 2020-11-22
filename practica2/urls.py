from django.contrib import admin
from django.urls import path
from practica2 import views

urlpatterns = [
    path('app/usuarios', views.getUsuarios),
]
