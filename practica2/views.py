from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from practica.models import *
from practica.serializers import *
from rest_framework.decorators import api_view
from datetime import datetime
import json
from dateutil.relativedelta import relativedelta

import urllib.request
import urllib.response
import requests
from django.shortcuts import render


def usuarios(request):
    if request.GET.get('mayores') == "True":
        usuarios = requests.get(
            "http://localhost:8080/api/usuarios?mayores=True").json()
        context = {"users": usuarios, "mostrando": "Mayores"}

    elif request.GET.get('mayores') == "False":
        usuarios = requests.get(
            "http://localhost:8080/api/usuarios?mayores=False").json()
        context = {"users": usuarios, "mostrando": "Menores"}

    else:
        usuarios = requests.get("http://localhost:8080/api/usuarios").json()
        context = {"users": usuarios, "mostrando": "Todos"}

    return render(request, 'usuarios.html', context)


def editarUsuarios(request, pk):
    usuario = requests.get(
        "http://localhost:8080/api/usuarios/"+str(pk)).json()
    context = {"user": usuario}
    return render(request, 'editarUsuario.html', context)

def listarPublicaciones(request, pk):
    usuario = requests.get(
        "http://localhost:8080/api/usuarios/"+str(pk)).json()
    publicaciones = requests.get("http://localhost:8080/api/usuarios/" + str(pk) + "/publicaciones").json()
    context = {"user": usuario, "publicaciones": publicaciones}
    return render(request, 'listarPublicaciones.html', context)

def editarPublicaciones(request, pk1, pk2):
    publicacion = requests.get(
        "http://localhost:8080/api/usuarios/"+str(pk1)+"/publicaciones/"+str(pk2)).json()
    context = {"publicacion": publicacion}
    return render(request, 'editarPublicacion.html', context)

def datosAbiertos(request):
    espacios = requests.get("http://localhost:8080/api/poiEAlt").json()
    context = {"espacios": espacios}
    return render(request, 'datosAbiertos.html', context)

def modificarComentario(request, pk1, pk2, pk3):
    comentario = request.get("http://localhost:8080/api/usuarios/" + str(pk1) + "/publicaciones/" + str(pk2) + "/comentarios/" + str(pk3)).json()
    publicacion = request.get("http://localhost:8080/api/usuarios/" + str(pk1) + "/publicaciones/" + str(pk2)).json()
    publicador = request.get("http://localhost:8080/api/usuarios/" + str(pk1)).json()
    context = {"comentario": comentario, "publicacion": publicacion, "publicador": publicador}
    return render(request, 'editarComentario.html', context)