from django.shortcuts import render, HttpResponse, get_object_or_404

from .forms import *
from .models import *

# Create your views here.

def libros(request,pk):
    libros = Libro.objects.all()
    return render(request, 'list_libros.html', {'lista':libros})

def autores(request,pk):
    autores = Autor.objects.all()

def prestamos(request,pk):
    prestamos = Prestamo.objects.all()

def add_libro(request):
    
    if request.method == 'POST':
        form = NewLibroForm(request.POST)
        if form.is_valid():
            post.save()
            return redirect('libros')
    else:
        form = NewLibroForm()
    return render(request, 'add_libro.html', {'form': form})

def add_autor(request):
    
    if request.method == 'POST':
        form = NewLibroForm(request.POST)
        if form.is_valid():
            post.save()
            return redirect('autores')
    else:
        form = NewLibroForm()
    return render(request, 'add_autor.html', {'form': form})

def add_prestamo(request):
    
    if request.method == 'POST':
        form = NewLibroForm(request.POST)
        if form.is_valid():
            post.save()
            return redirect('prestamos')
    else:
        form = NewLibroForm()
    return render(request, 'add_prestamo.html', {'form': form})

def edit_libro(request,pk):
    pass

def edit_autor(request,pk):
    pass

def edit_prestamo(request,pk):
    pass

def delete_libro(request,pk):
    pass

def delete_autor(request,pk):
    pass

def delete_prestamo(request,pk):
    pass
