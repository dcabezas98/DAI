from django.core.exceptions import ValidationError
from django import forms
from .models import *
import datetime


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ('titulo', 'portada')

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ('nombre', 'obras')

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields= ('libro', 'fecha', 'usuario')
    def clean_fecha(self):
        data=self.cleaned_data['fecha']
        if data<datetime.date.today():
            raise ValidationError('La fecha no puede ser pasada', code='fecha_pasada')
        return data
