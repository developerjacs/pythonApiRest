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
        try:
            usuario_data = request.POST.dict()  # Caso form
        except:
            usuario_data = JSONParser().parse(request)  # Caso json

        usuario_data["fecha_registro"] = datetime.today().strftime('%Y-%m-%d')
        usuarios_serializer = UsuarioSerializer(data=usuario_data)
        print("llege")
        if usuarios_serializer.is_valid():
            usuarios_serializer.save()
            return JsonResponse(usuarios_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(usuarios_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Funciones de Fran
# api/usuarios/{id}   -> get, update, delete
# api/usuarios/{id}/publicaciones   -> get, post    FRAN
# api/usuarios/{id}/publicaciones/{id}   -> get, delete, update


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def getUsuarioId(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return JsonResponse({'message': 'The usuario does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        usuario_serializer = UsuarioSerializer(usuario)
        return JsonResponse(usuario_serializer.data)
    elif request.method == 'POST':
        if request.POST.get('method') == "PUT":
            try:
                usuario_data = request.POST.dict()  # Caso form
            except:
                usuario_data = JSONParser().parse(request)  # Caso json

            usuario_serializer = UsuarioSerializer(usuario, data=usuario_data)
            if usuario_serializer.is_valid():
                usuario_serializer.save()
                return JsonResponse(usuario_serializer.data)
            return JsonResponse(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.POST.get('method') == "DELETE":
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
        try:
            publicacion = request.POST.dict()  # Caso form
        except:
            publicacion = JSONParser().parse(request)  # Caso json
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
    elif request.method == 'POST':
        if request.POST.get('method') == 'PUT':
            try:
                publicacion_data = request.POST.dict()  # Caso form
            except:
                publicacion_data = JSONParser().parse(request)  # Caso json
            publicacion_data['fecha'] = datetime.today().strftime(
                '%Y-%m-%dT%H:%M:%S')
            publicacion_serializer = PublicacionSerializer(
                publicacion, data=publicacion_data)
            if publicacion_serializer.is_valid():
                publicacion_serializer.save()
                return JsonResponse(publicacion_serializer.data)
            return JsonResponse(publicacion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.POST.get('method') == 'DELETE':
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
        try:
            comentario = request.POST.dict()  # Caso form
        except:
            comentario = JSONParser().parse(request)  # Caso json
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
        publicaciones_serializer = PublicacionSerializer(
            publicaciones_objects, many=True)
        return JsonResponse(publicaciones_serializer.data, safe=False, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        publicacion_data = JSONParser().parse(request)
        publicacion_data['fecha'] = datetime.today().strftime(
            '%Y-%m-%dT%H:%M:%S')
        print(publicacion_data['fecha'])
        publicacion_data['ubicacion'] = 'locationPlaceholder'
        publicacion_serializada = PublicacionSerializer(data=publicacion_data)
        if publicacion_serializada.is_valid():
            publicacion_serializada.save()
            return JsonResponse(publicacion_serializada.data, status=status.HTTP_201_CREATED)
        return JsonResponse(publicacion_serializada.errors, status=status.HTTP_400_BAD_REQUEST)

# Funciones de Noel
@api_view(['GET', 'POST'])
def getComentarios(request):
    if request.method == 'GET':
        comentarios = Comentario.objects.all()
        comentarios_serializer = ComentarioSerializer(comentarios, many=True)
        return JsonResponse(comentarios_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        comentario_data = JSONParser().parse(request)
        comentario_data["fecha"] = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
        comentarios_serializer = ComentarioSerializer(data=comentario_data)
        if comentarios_serializer.is_valid():
            comentarios_serializer.save()
            return JsonResponse(comentarios_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(comentarios_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE','POST'])
def getComentariosID(request, pk):
    try:
        comentario = Comentario.objects.get(pk=pk)
    except Comentario.DoesNotExist:
        return JsonResponse({'message': 'The comentario does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        comentario_serializer = ComentarioSerializer(comentario)
        return JsonResponse(comentario_serializer.data)
    elif request.method == 'POST':
        if request.POST.get('method') == 'PUT':
            try:
                comentario_data = request.POST.dict()  # Caso form
            except:
                comentario_data = JSONParser().parse(request)  # Caso json
            comentario_serializer = ComentarioSerializer(
                comentario, data=comentario_data)
            if comentario_serializer.is_valid():
                comentario_serializer.save()
                return JsonResponse(comentario_serializer.data)
            return JsonResponse(comentario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.POST.get('method') == 'DELETE':
            comentario.delete()
            return JsonResponse({'message': 'Comentario was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def getPublicacionesID(request, pk):
    try:
        publicacion = Publicacion.objects.get(pk=pk)
    except Publicacion.DoesNotExist:
        return JsonResponse({'message': 'The publicacion does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        publicacion_serializer = PublicacionSerializer(publicacion)
        return JsonResponse(publicacion_serializer.data)
    elif request.method == 'PUT':
        publicacion_data = JSONParser().parse(request)
        publicacion_serializer = PublicacionSerializer(
            publicacion, data=publicacion_data)
        if publicacion_serializer.is_valid():
            publicacion_serializer.save()
            return JsonResponse(publicacion_serializer.data)
        return JsonResponse(publicacion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        publicacion.delete()
        return JsonResponse({'message': 'Publicacion was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)



# Funciones de German 
@api_view(['GET'])
def getPOIEspaciosAlt(request):
    if request.method == 'GET':
        url = 'https://datosabiertos.malaga.eu/api/3/action/datastore_search?resource_id=c9c73aca-26e9-4f89-b7c6-59db49346243'
        resultado = requests.get(url)

        return (JsonResponse(resultado.json(),safe=False, status= requests.get(url).status_code))


@api_view(['GET'])
def getPOIbyTitleEspaciosAlt(request, title):
    if request.method == 'GET':
        url = 'https://datosabiertos.malaga.eu/api/3/action/datastore_search?resource_id=c9c73aca-26e9-4f89-b7c6-59db49346243&limit=5&filters=%7B%22NOMBRE%22:%22'+ title +'%22}'

        resultado = requests.get(url)

        return (JsonResponse(resultado.json(),safe=False, status= requests.get(url).status_code))

@api_view(['GET'])
def getPOIbyIdEspaciosAlt(request, id):
    if request.method == 'GET':
        url = 'https://datosabiertos.malaga.eu/api/3/action/datastore_search?resource_id=c9c73aca-26e9-4f89-b7c6-59db49346243&limit=5&filters=%7B%22ID%22:%22'+ id +'%22}'  #Id es un int 4
        resultado = requests.get(url)

        return (JsonResponse(resultado.json(), safe=False, status=requests.get(url).status_code))

@api_view(['GET'])
def getPOICentrosCulturales(request):
    if request.method == 'GET':
        url = 'https://datosabiertos.malaga.eu/api/3/action/datastore_search?resource_id=7e0ae247-36ab-4dd5-8df2-f0392289441f'
        resultado = requests.get(url)

        return (JsonResponse(resultado.json(), safe=False, status=requests.get(url).status_code))
@api_view(['GET'])
def getPOIbyTitleCentrosCulturales(request, title):
    if request.method == 'GET':
        url = 'https://datosabiertos.malaga.eu/api/3/action/datastore_search?resource_id=7e0ae247-36ab-4dd5-8df2-f0392289441f&limit=5&filters=%7B%22NOMBRE%22:%22'+ title +'%22}'
        resultado = requests.get(url)

        return (JsonResponse(resultado.json(), safe=False, status=requests.get(url).status_code))

@api_view(['GET'])
def getPOIbyIdCentrosCulturales(request, id):
    if request.method == 'GET':
        url = 'https://datosabiertos.malaga.eu/api/3/action/datastore_search?resource_id=7e0ae247-36ab-4dd5-8df2-f0392289441f&limit=5&filters=%7B%22ID%22:%22'+ id +'%22}'
        resultado = requests.get(url)

        return (JsonResponse(resultado.json(), safe=False, status=requests.get(url).status_code))