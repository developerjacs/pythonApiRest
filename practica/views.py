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

#Funciones de Fran
#api/usuarios/{id}   -> get, update, delete
#api/usuarios/{id}/publicaciones   -> get, post    FRAN
#api/usuarios/{id}/publicaciones/{id}   -> get, delete, update
@api_view(['GET', 'PUT', 'DELETE'])
def getUsuarioId(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return JsonResponse({'message': 'The usuario does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        usuario_serializer = UsuarioSerializer(usuario)
        return JsonResponse(usuario_serializer.data)
    elif request.method == 'PUT':
        usuario_data = JSONParser().parse(request)
        usuario_serializer = UsuarioSerializer(usuario, data=usuario_data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return JsonResponse(usuario_serializer.data)
        return JsonResponse(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        usuario.delete()
        return JsonResponse({'message': 'Usuario was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def publicaciones_list(request, pk):
    if request.method == 'GET':
        try:
            publicaciones = Publicacion.objects.filter(publicador=pk)
        except Publicacion.DoesNotExist:
            return JsonResponse({'message': 'Usuario with specified id does not exist'}, status=status.HTTP_204_NO_CONTENT)
        serializados = PublicacionSerializer(publicaciones, many=True)
        return JsonResponse(serializados.data, safe=False, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        publicacion = JSONParser().parse(request)
        publicacion['fecha'] = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
        publicacion['publicador'] = pk
        publicacion_serializada = PublicacionSerializer(data=publicacion)
        if publicacion_serializada.is_valid():
            publicacion_serializada.save()
            return JsonResponse(publicacion_serializada.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(publicacion_serializada.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def getPublicacionId(request, pk1, pk2):
    try:
        publicaciones_del_usuario = Publicacion.objects.filter(publicador=pk1)
        publicacion = publicaciones_del_usuario.get(pk=pk2)
    except Publicacion.DoesNotExist:
        return JsonResponse({'message': 'The publicacion does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        publicacion_serializer = PublicacionSerializer(publicacion)
        return JsonResponse(publicacion_serializer.data)
    elif request.method == 'PUT':
        publicacion_data = JSONParser().parse(request)
        publicacion_data['fecha'] = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
        publicacion_serializer = PublicacionSerializer(publicacion, data=publicacion_data)
        if publicacion_serializer.is_valid():
            publicacion_serializer.save()
            return JsonResponse(publicacion_serializer.data)
        return JsonResponse(publicacion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        publicacion.delete()
        return JsonResponse({'message': 'Publicacion was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

# Funciones de Romolo
@api_view(['GET', 'POST', 'DELETE'])
def comentarios_publicacion(request, pk):
    if request.method == 'GET':
        try:
            comentarios = Comentario.objects.filter(publicacion=pk)
        except Comentario.DoesNotExist:
            return JsonResponse({'message': 'Publicacion with specified id does not exist'}, status=status.HTTP_204_NO_CONTENT)
        serializados = ComentarioSerializer(comentarios, many=True)
        return JsonResponse(serializados.data, safe=False, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        comentario = JSONParser().parse(request)
        comentario['fecha'] = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
        comentario['publicacion'] = pk
        print(comentario['publicacion'])
        serializado = ComentarioSerializer(data=comentario)
        if serializado.is_valid():
            serializado.save()
            return JsonResponse(serializado.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializado.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def publicaciones(request):
    if request.method == 'GET':
        publicaciones_objects = Publicacion.objects.all()
        publicaciones_serializer = PublicacionSerializer(publicaciones_objects, many=True)
        return JsonResponse(publicaciones_serializer.data, safe=False, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        publicacion_data = JSONParser().parse(request)
        publicacion_data['fecha'] = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
        print(publicacion_data['fecha'])
        publicacion_data['ubicacion'] = 'locationPlaceholder'
        publicacion_serializada = PublicacionSerializer(data=publicacion_data)
        if publicacion_serializada.is_valid():
            publicacion_serializada.save()
            return JsonResponse(publicacion_serializada.data, status=status.HTTP_201_CREATED)
        return JsonResponse(publicacion_serializada.errors, status=status.HTTP_400_BAD_REQUEST)

