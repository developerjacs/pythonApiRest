from django.contrib import admin
from django.urls import path
from practica2 import views

urlpatterns = [
    path('app/usuarios', views.usuarios),
    path('app/editarUsuario/<pk>', views.editarUsuarios),
    path('app/datosAbiertos', views.datosAbiertos),
    path('app/usuarios/<pk>/listarPublicaciones', views.listarPublicaciones),
    path('app/usuarios/<pk1>/editarPublicacion/<pk2>', views.editarPublicaciones),
    path('app/publicaciones/<pk>/listarComentarios', views.listarComentarios),
]
