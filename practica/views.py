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


@api_view(['GET', 'POST'])
def getUsuarios(request):
    if request.method == 'GET':
        if request.GET.get('mayores') == "False":
            fecha_minima = datetime.now() - relativedelta(years=18)
            usuarios = Usuario.objects.filter(
                fecha_nacimiento__gte=fecha_minima)
            usuarios_serializer = UsuarioSerializer(usuarios, many=True)
            return JsonResponse(usuarios_serializer.data, safe=False, status=status.HTTP_200_OK)

        elif request.GET.get('mayores') == "True":
            fecha_minima = datetime.now() - relativedelta(years=18)
            usuarios = Usuario.objects.filter(
                fecha_nacimiento__lte=fecha_minima)
            usuarios_serializer = UsuarioSerializer(usuarios, many=True)
            return JsonResponse(usuarios_serializer.data, safe=False, status=status.HTTP_200_OK)

        else:
            usuarios = Usuario.objects.all()
            usuarios_serializer = UsuarioSerializer(usuarios, many=True)
            return JsonResponse(usuarios_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        usuario_data = JSONParser().parse(request)
        usuario_data["fecha_registro"] = datetime.today().strftime('%Y-%m-%d')
        usuarios_serializer = UsuarioSerializer(data=usuario_data)
        if usuarios_serializer.is_valid():
            usuarios_serializer.save()
            return JsonResponse(usuarios_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(usuarios_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Funciones de Romolo
@api_view(['GET', 'UPDATE', 'DELETE'])
def comentarios_publicacion(request, idUsuario, idPublicacion):
    pass