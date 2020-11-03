#./app/app.py
from flask import Flask, render_template, session, request
from pickleshare import *
from ejercicios import *
from generateSVG import randSVG

app = Flask(__name__)
app.secret_key='esto-es-una-clave-muy-secreta'

# Página principal, con índice
@app.route('/')
def index():
    return render_template('index.html')

#Login
@app.route('/login', methods=['POST'])
def login():
    user = request.form['user']
    passwd = request.form['password']
    session['user']=user
    #TODO

# Ejercicio 2: Algoritmos de ordenación

# Ordenación por burbuja
@app.route('/bubblesort/<l>')
def bubbleSort(l):
    l1, t = bubble_sort(l)
    l1 = list(map(str,l1))
    l1 = ', '.join(l1)
    return render_ejer('Bubble Sort:',l,l1+'.  '+'Time: '+str(t)+' seconds.')

# Ordenación por selección
@app.route('/selectionsort/<l>')
def selectionSort(l):
    l1, t = selection_sort(l)
    l1 = list(map(str,l1))
    l1 = ', '.join(l1)
    return render_ejer('Selection Sort:',l,l1+'.  '+'Time: '+str(t)+' seconds.')

# Ordenación por inserción
@app.route('/insertionsort/<l>')
def insertionSort(l):
    l1, t = insertion_sort(l)
    l1 = list(map(str,l1))
    l1 = ', '.join(l1)
    return render_ejer('Insertion Sort:',l,l1+'.  '+'Time: '+str(t)+' seconds.')

# Ejercicio 3: Criba de Erastóstenes
@app.route('/erastosthenes/<n>')
def erastosthenes(n):
    n = int(n)
    if n<0:
        return render_ejer('Criba de Erastóstenes:',str(n),'Incorrect input!')
    
    prime = erastosthenes_sieve(n)
    prime = ', '.join(prime)
    return render_ejer('Criba de Erastóstenes:',str(n),prime)

# Ejercicio 4: Fibonacci
@app.route('/fibonacci/<n>')
def fibonacci(n):
    n = int(n)
    if n<=0:
        return render_ejer('Fibonacci:',str(n),'Incorrect input!')
    
    return render_ejer('Fibonacci:',str(n),str(fibo(n)))

# Ejercicio 5: Corchetes
@app.route('/corchetes/<l>')
def corchetes(l):
    return render_ejer('Corchetes', l, brackets(l))

# Ejercicio 6: Expresiones regulares

# Cualquier palabra seguida de un espacio y una única letra mayúscula
@app.route('/re/<cadena>')
def wordCapital(cadena):
    match = word_capital(cadena)
    return render_ejer('Expresiones regulares: Palabra seguida de espacio y una única letra mayúscula',cadena,', '.join(match))

# Identificar correos electrónicos válidos
@app.route('/emails/<cadena>')
def emails(cadena):
    match = e_mails(cadena)
    return render_ejer('Expresiones regulares: Correos electrónicos válidos',cadena,', '.join(match))

# Identificar números de tarjeta de crédito
@app.route('/creditcards/<cadena>')
def creditcards(cadena):
    match = credit_cards(cadena)
    return render_ejer('Expresiones regulares: Números de tarjeta de crédito',cadena,', '.join(match))

# Random SVG
@app.route('/svg')
def random_svg():
    randsvg=randSVG()

    if randsvg[0] == 1:
        return render_template('SVGellipse.html', cx=randsvg[1],
                               cy=randsvg[2], rx=randsvg[3],
                               ry=randsvg[4], fill=randsvg[5])
    elif randsvg[0] == 2:
        return render_template('SVGrectangle.html', x=randsvg[1],
                               y=randsvg[2], width=randsvg[3],
                               height=randsvg[4], fill=randsvg[5])
    
# Manejador de error 404: URL no definida
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Plantilla para template hijo
def render_ejer(name, inpt, content):
    return render_template('ejer.html', nombre=name, entrada=inpt, contenido=content)
