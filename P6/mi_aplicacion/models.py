# mi_aplicacion/models.py

"""
Cada vez que se modifique la estructura de las tablas:
docker-compose run web python manage.py makemigrations mi_aplicacion
docker-compose run web python manage.py migrate mi_aplicacion 
"""

from django.db import models
from django.utils import timezone

# Create your models here.

class Libro(models.Model):
  titulo = models.CharField(max_length=200)
  portada = models.ImageField(upload_to='covers', default='default-cover.jpg')

  def __str__(self):
    return self.titulo

class Prestamo(models.Model):
  libro   = models.ForeignKey(Libro, on_delete=models.CASCADE)
  fecha   = models.DateField(default=timezone.now)
  usuario = models.CharField(max_length=100)

class Autor(models.Model):
  nombre = models.CharField(max_length=100)
  obras = models.ManyToManyField(Libro)

  class Meta:
        verbose_name_plural = "Autores"

  def __srt__(self):
    return self.nombre
