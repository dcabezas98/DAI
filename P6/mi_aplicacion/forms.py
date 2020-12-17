from django import forms
from .models import *
from django.utils import timezone

class NewLibroForm(forms.Form):
    titulo = forms.CharField(help_text="Título")
    portada = forms.ImageField(help_text="Portada", required=False)

class NewAutorForm(forms.Form):
    nombre = forms.CharField(help_text="Nombre")

class NewPrestamoForm(forms.Form):
    libro   = forms.CharField(help_text="Libro")
    fecha   = forms.DateField(initial=timezone.now)
    usuario = forms.CharField(help_text="Usuario")
