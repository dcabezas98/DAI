import time
import re

# Ejercicio 2: Algoritmos de ordenación

# Ordenación por burbuja
def bubble_sort(l):
    l = l.split(',')
    l = list(map(int,l))
    n = len(l)

    start = time.process_time()

    for i in range(n-1):
        for j in range(n-i-1):
            if l[j] > l[j+1]:
                l[j], l[j+1] = l[j+1], l[j]

    t = time.process_time() - start

    return l, t

# Ordenación por selección
def selection_sort(l):
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

    return l, t

# Ordenación por inserción
def insertion_sort(l):
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

    return l, t

# Ejercicio 3: Criba de Erastóstenes
def erastosthenes_sieve(n):

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

    return prime

# Ejercicio 4: Fibonacci
def fibo(n):
    if n==1:
        return 0
    elif n==2:
        return 1
    else:
        return fibo(n-1)+fibo(n-2)

# Ejercicio 5: Corchetes
def brackets(l):
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
def word_capital(cadena):
    return re.findall(r'\w+ [A-Z](?!\w)',cadena)

# Identificar correos electrónicos válidos
def e_mails(cadena):
    match = re.findall(r'(?<=\s|\:)(\w+(\.\w+)*@\w+(\.\w+)+)(?=\.|\s|,)',cadena)
    return [m[0] for m in match]

# Identificar números de tarjeta de crédito
def credit_cards(cadena):
    return re.findall(r'(?<![0-9])([0-9]{4} [0-9]{4} [0-9]{4} [0-9]{4}|[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4})(?![0-9])',cadena)
