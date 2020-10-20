#./app/app.py
from flask import Flask, render_template
from ejercicios import *


app = Flask(__name__)

# Página principal, con índice
@app.route('/')
def index():
    return render_template('index.html')

# Ejercicio 2: Algoritmos de ordenación

# Ordenación por burbuja
@app.route('/bubblesort/<l>')
def bubbleSort(l):
    l, t = bubble_sort(l)
    l = list(map(str,l))
    l = ', '.join(l)
    return l+'<br/>'+'Time: '+str(t)+' seconds.'

# Ordenación por selección
@app.route('/selectionsort/<l>')
def selectionSort(l):
    l, t = selection_sort(l)
    l = list(map(str,l))
    l = ', '.join(l)
    return l+'<br/>'+'Time: '+str(t)+' seconds.'

# Ordenación por inserción
@app.route('/insertionsort/<l>')
def insertionSort(l):
    l, t = insertion_sort(l)
    l = list(map(str,l))
    l = ', '.join(l)
    return l+'<br/>'+'Time: '+str(t)+' seconds.'

# Ejercicio 3: Criba de Erastóstenes
@app.route('/erastosthenes/<n>')
def erastosthenes(n):
    n = int(n)
    if n<0:
        return 'Incorrect input!'
    
    prime = erastosthenes_sieve(n)
    prime = ', '.join(prime)
    return prime

# Ejercicio 4: Fibonacci
@app.route('/fibonacci/<n>')
def fibonacci(n):
    n = int(n)
    if n<=0:
        return 'Incorrect input!'
    
    return str(fibo(n))

# Ejercicio 5: Corchetes
@app.route('/corchetes/<l>')
def corchetes(l):
    return brackets(l)

# Ejercicio 6: Expresiones regulares

# Cualquier palabra seguida de un espacio y una única letra mayúscula
@app.route('/re/<cadena>')
def wordCapital(cadena):
    match = word_capital(cadena)
    return cadena+'<br/><br/>'+', '.join(match)

# Identificar correos electrónicos válidos
@app.route('/emails/<cadena>')
def emails(cadena):
    match = e_mails(cadena)
    return cadena+'<br/><br/>'+', '.join(match)

# Identificar números de tarjeta de crédito
@app.route('/creditcards/<cadena>')
def creditcards(cadena):
    match = credit_cards(cadena)
    return cadena+'<br/><br/>'+', '.join(match)

# Manejador de error 404: URL no definida
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
