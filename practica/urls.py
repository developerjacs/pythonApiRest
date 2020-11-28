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
    path('api/poiEAlt', views.getPOIEspaciosAlt),
    path('api/poiEAlt/id/<id>', views.getPOIbyIdEspaciosAlt),
    path('api/poiEAlt/nombre/<title>', views.getPOIbyTitleEspaciosAlt),
    path('api/poiCCul', views.getPOICentrosCulturales),
    path('api/poiCCul/id/<id>', views.getPOIbyIdCentrosCulturales),
    path('api/poiCCul/nombre/<title>', views.getPOIbyTitleCentrosCulturales),
    path('api/comentarios', views.getComentarios),
    path('api/comentarios/<pk>', views.getComentariosID),
    path('api/publicaciones/<pk>', views.getPublicacionesID),
]
