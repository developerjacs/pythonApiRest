from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=70, blank=False, default='')
    apellido1 = models.CharField(max_length=70, blank=False, default='')
    apellido2 = models.CharField(max_length=70, blank=False, default='')
    nombre_usuario = models.CharField(max_length=70, blank=False, default='')
    fecha_nacimiento = models.DateField(blank=True)
    fecha_registro = models.DateField(blank=True)
    biografia = models.CharField(max_length=150, blank=True)
    
    seguidos = models.ManyToManyField('Usuario', blank=True)

class Publicacion(models.Model):
    nombre = models.CharField(max_length=70, blank=False, default='')
    descripcion = models.CharField(max_length=200, blank=False, default='')
    graffiti = models.CharField(max_length=70,blank=False, default='')
    fecha = models.DateTimeField(blank=False)
    autor =  models.CharField(max_length=70, blank=False, default='')
    ubicacion = models.CharField(max_length=70, blank=False, default='')
    
    likes = models.ManyToManyField(Usuario, 'Likes', blank=True)
    publicador = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class Comentario(models.Model):
    mensaje = models.CharField(max_length=70, blank=False, default='')
    fecha = models.DateTimeField(blank=False)

    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, blank=False)
    publicador = models.ForeignKey(Usuario, on_delete=models.CASCADE)