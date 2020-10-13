#./app/app.py
from flask import Flask, render_template
import time
import re

app = Flask(__name__)

# Página para URLs inválidas
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'Lo siento, la URL que buscas no existe.'

# Página principal, con índice
@app.route('/')
def index():
    return render_template('index.html')

# Ejercicio 2: Algoritmos de ordenación

# Ordenación por burbuja
@app.route('/bubblesort/<l>')
def bubbleSort(l):
    l = l.split(',')
    l = list(map(int,l))
    n = len(l)

    start = time.process_time()

    for i in range(n-1):
        for j in range(n-i-1):
            if l[j] > l[j+1]:
                l[j], l[j+1] = l[j+1], l[j]

    t = time.process_time() - start

    l = list(map(str,l))
    l = ', '.join(l)
    
    return l+'<br/>'+'Time: '+str(t)+' seconds.'

# Ordenación por selección
@app.route('/selectionsort/<l>')
def selectionSort(l):
    l = l.split(',')
    l = list(map(int,l))
    n = len(l)

    start = time.process_time()
    
    for i in range(n):
        min_index = i
        for j in range(i+1,n):
            if l[min_index] > l[j]:
                min_index = j

        l[i], l[min_index] = l[min_index], l[i]

    t = time.process_time() - start

    l = list(map(str,l))
    l = ', '.join(l)
    
    return l+'<br/>'+'Time: '+str(t)+' seconds.'

# Ordenación por inserción
@app.route('/insertionsort/<l>')
def insertionSort(l):
    l = l.split(',')
    l = list(map(int,l))
    n = len(l)

    start = time.process_time()
    
    for i in range(1,n):
        key = l[i]
        j = i-1
        while j>=0 and key<l[j]:
            l[j+1] = l[j]
            j -= 1
        l[j+1] = key

    t = time.process_time() - start

    l = list(map(str,l))
    l = ', '.join(l)
    
    return l+'<br/>'+'Time: '+str(t)+' seconds.'

# Ejercicio 3: Criba de Erastóstenes
@app.route('/erastosthenes/<n>')
def erastostenes(n):
    n = int(n)

    if n < 0:
        return 'Incorrect input!'

    prime = [True for i in range(n)]
    p = 2
    while(p*p < n):
        if (prime[p]): # p is prime
            for i in range(p*2, n, p):
                prime[i] = False

        p += 1

    if n >= 1:
        prime[0] = False
    if n >= 2:
        prime[1] = False

    prime = [str(idx) for idx, isp in enumerate(prime) if isp]

    prime = ', '.join(prime)

    return prime

# Ejercicio 4: Fibonacci
@app.route('/fibonacci/<n>')
def fibonacci(n):
    n = int(n)

    if n <= 0:
        return 'Incorrect input!'
    elif n==1:
        return '0'
    elif n==2:
        return '1'
    else:
        return str(int(fibonacci(n-1))+int(fibonacci(n-2)))

# Ejercicio 5: Corchetes
@app.route('/corchetes/<l>')
def corchetes(l):
    
    abiertos = 0

    for i in l:
        if i == '[':
            abiertos +=1
        elif i == ']':
            abiertos -= 1
        else:
            return 'Incorrect input!'

        if abiertos < 0:
            return 'Los corchetes NO están bien anidados.'

    if abiertos != 0:
        return 'Los corchetes NO están bien anidados.'
    return 'Los corchetes están bien anidados.'

# Ejercicio 6: Expresiones regulares

# Cualquier palabra seguida de un espacio y una única letra mayúscula
@app.route('/re/<cadena>')
def wordUpper(cadena):
    match = re.findall(r'\w+ [A-Z](?!\w)',cadena)
    return cadena+'<br/><br/>'+', '.join(match)

# Identificar correos electrónicos válidos
@app.route('/emails/<cadena>')
def emails(cadena):
    match = re.findall(r'(?<=\s|\:)(\w+(\.\w+)*@\w+(\.\w+)+)(?=\.|\s|,)',cadena)
    match = [m[0] for m in match]
    return cadena+'<br/><br/>'+', '.join(match)

# Identificar números de tarjeta de crédito
@app.route('/creditcards/<cadena>')
def creditcards(cadena):
    match = re.findall(r'(?<![0-9])([0-9]{4} [0-9]{4} [0-9]{4} [0-9]{4}|[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4})(?![0-9])',cadena)
    return cadena+'<br/><br/>'+', '.join(match)

