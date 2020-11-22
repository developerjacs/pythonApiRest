from rest_framework import serializers 
from practica.models import *
 
 
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id',
                  'nombre',
                  'apellido1',
                  'apellido2', 
                  'nombre_usuario',
                  'fecha_nacimiento',
                  'fecha_registro',
                  'biografia',
                  'seguidos')

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion 
        fields = ('id',
                  'nombre',
                  'descripcion',
                  'graffiti',
                  'fecha',
                  'autor',
                  'ubicacion',
                  'likes',
                  'publicador')
    
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ('id',
                  'mensaje',
                  'fecha',
                  'publicacion',
                  'publicador')
    




    