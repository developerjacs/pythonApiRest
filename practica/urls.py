from django.contrib import admin
from django.urls import path
from practica import views

urlpatterns = [
    path('api/usuarios', views.getUsuarios),
    path('api/usuarios/<pk>', views.getUsuarioId),
    path('api/usuarios/<pk>/publicaciones', views.publicaciones_list),
    path('api/usuarios/<pk1>/publicaciones/<pk2>', views.getPublicacionId),
    path('api/publicaciones/<pk>/comentarios', views.comentarios_publicacion),
    path('api/publicaciones', views.publicaciones),
]
