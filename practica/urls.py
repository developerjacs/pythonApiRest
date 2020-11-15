from django.contrib import admin
from django.urls import path
from practica import views

urlpatterns = [
    path('api/usuarios', views.getUsuarios),
    path('api/publicaciones/<int:pk>/comentarios', views.comentarios_publicacion),
]
