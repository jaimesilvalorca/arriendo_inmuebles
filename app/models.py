from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class TipoInmueble(models.Model):
    tipo_inmueble = models.TextField()

class Comuna(models.Model):
    comuna = models.TextField()

class Region(models.Model):
    region = models.TextField()

class TipoUser(models.Model):
    tipo_user = models.TextField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_tipo_user = models.ForeignKey(TipoUser, on_delete=models.CASCADE, null=True)
    rut = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=12)
    correo = models.CharField(max_length=50)

class Inmuebles(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id_tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete=models.CASCADE, null=True)
    id_comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, null=True)
    id_region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    nombre_inmueble = models.TextField()
    descripcion = models.CharField(max_length=200)
    terreno_construido = models.FloatField()
    terreno = models.FloatField()
    numero_estacionamientos = models.PositiveIntegerField(default=0)
    numero_banos = models.PositiveIntegerField(default=0)
    numero_habitaciones = models.PositiveIntegerField(default=0)
    direccion = models.CharField(max_length=200)
    precio_mensual = models.PositiveIntegerField()
    imagen = models.CharField(max_length=200, null=True)
    estado = models.BooleanField(default=False)