# mi_aplicacion/urls.py

from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add_libro/$', views.add_libro, name='add_libro'),
    url(r'^add_autor/$', views.add_autor, name='add_autor'),
    url(r'^add_prestamo/$', views.add_prestamo, name='add_prestamo'),
    url(r'^libros/$', views.libros, name='list_libros'),
    url(r'^autores/$', views.autores, name='list_autores'),
    url(r'^prestamos/$', views.prestamos, name='list_prestamos'),
    path('edit_libro/<int:pk>', views.edit_libro, name='edit_libro'),
    path('edit_autor/<int:pk>', views.edit_autor, name='edit_autor'),
    path('edit_prestamo/<int:pk>', views.edit_prestamo, name='edit_prestamo'),
    path('delete_libro/<int:pk>', views.delete_libro, name='delete_libro'),
    path('delete_autor/<int:pk>', views.delete_autor, name='delete_autor'),
    path('delete_prestamo/<int:pk>', views.delete_prestamo, name='delete_prestamo')
]
