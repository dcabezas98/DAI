from django.contrib import admin

# Register your models here.

from .models import Libro, Autor, Prestamo

admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Prestamo)
