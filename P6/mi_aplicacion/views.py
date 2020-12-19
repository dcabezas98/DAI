from django.shortcuts import render, HttpResponse, redirect

from .forms import *
from .models import *

# Create your views here.

def home(request):
    return redirect('list_libros')

def libros(request):
    libros = Libro.objects.all()
    libros2=[]
    for libro in libros:
        autores=libro.autor_set.all()
        libros2.append(dict({'titulo':libro.titulo, 'portada':libro.portada, 'id':libro.id, 'autores':[autor.nombre for autor in autores]}))
    return render(request, 'list_libros.html', {'lista':libros2, 'n':libros.count()})

def autores(request):
    autores = Autor.objects.all()
    return render(request, 'list_autores.html', {'lista':autores, 'n':autores.count()})

def prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'list_prestamos.html', {'lista':prestamos, 'n':prestamos.count()})

def add_libro(request):

    form = LibroForm()
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_libros')

    return render(request, 'add_libro.html', {'form': form})

def add_autor(request):

    form = AutorForm()
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_autores')
        
    return render(request, 'add_autor.html', {'form': form})

def add_prestamo(request):

    form = PrestamoForm()
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_prestamos')
        
    return render(request, 'add_prestamo.html', {'form': form})

def edit_libro(request,pk):
    instancia = Libro.objects.get(id=pk)
    form = LibroForm(instance=instancia)
    if request.method=="POST":
        form = LibroForm(request.POST, request.FILES, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('list_libros')

    return render(request, 'edit_libro.html', {'form':form})
    
def edit_autor(request,pk):
    instancia = Autor.objects.get(id=pk)
    form = AutorForm(instance=instancia)
    if request.method=="POST":
        form = AutorForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('list_autores')

    return render(request, 'edit_autor.html', {'form':form})

def edit_prestamo(request,pk):
    instancia = Prestamo.objects.get(id=pk)
    form = PrestamoForm(instance=instancia)
    if request.method=="POST":
        form = PrestamoForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('list_prestamos')

    return render(request, 'edit_prestamo.html', {'form':form})

def delete_libro(request,pk):
    instancia = Libro.objects.get(id=pk)
    instancia.delete()
    return redirect('list_libros')

def delete_autor(request,pk):
    instancia = Autor.objects.get(id=pk)
    instancia.delete()
    return redirect('list_autores')

def delete_prestamo(request,pk):
    instancia = Prestamo.objects.get(id=pk)
    instancia.delete()
    return redirect('list_prestamos')
