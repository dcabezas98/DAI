#./app/app.py
from flask import Flask, render_template, session, request, flash, redirect, url_for
from model import *
from ejercicios import *
from random import randint
from generateSVG import randSVG

app = Flask(__name__)
app.secret_key='esto-es-una-clave-muy-secreta'

# Página principal, con índice
@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    store_visted_urls(request.url, 'Home')
    return render_template('home.html')

# Login
@app.route('/login', methods=['POST'])
def login():
    user = request.form['user']
    passwd = request.form['passwd']
    
    if checkUser(user):
        if passwd == getUser(user)['passwd']:
            session['user']=user
            session['urls'] = []
            session['names']= []
            flash(user+' loguead@ con éxito :D')
        else:
            flash('Contraseña Incorrecta :(')
    else:
        flash('Usuario no registrado :(')

    return redirect(url_for('home'))

# Registro
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form['user']
        passwd = request.form['passwd']
        color = request.form['color']
        if not checkUser(user):          
            session['user']=user
            session['urls'] = []
            session['names']= []
            addUser(user,{'passwd':passwd, 'color':color})
            flash(user+' registrad@ con éxito :D')
        else:
            flash(user+' ya está registrad@ >:(')
        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    flash('Hasta pronto '+session['user']+'!')
    session['user']=''
    return redirect(url_for('home'))

@app.route('/user')
def user():
    store_visted_urls(request.url, 'User')
    return render_template('user.html', user=getUser(session['user']))

@app.route('/change', methods=['GET','POST'])
def change():
    if request.method == 'POST':
        user = request.form['user']
        passwd = request.form['passwd']
        color = request.form['color']

        if user == session['user'] or not checkUser(user):
            delUser(session['user']) # Borro el antiguo usuario
            addUser(user,{'passwd':passwd, 'color':color}) # Creo el nuevo
            session['user']=user
            flash('Cambios guardados con éxito :)')
            return redirect(url_for('home'))
        else:
            flash(user+' ya está registrad@, no se han guardado los cambios >:(')
            return redirect(url_for('change'))

    store_visted_urls(request.url, 'Edit')
    return render_template('change.html', user=getUser(session['user']))

@app.route('/delete')
def delete():
    delUser(session['user'])
    flash('El usuario '+session['user']+' ha sido eliminado')
    session['user']=''
    return redirect(url_for('home'))

def store_visted_urls(url, name):
    if 'urls' in session:
        session['urls']=[url]+session['urls']
        session['names']=[name]+session['names']
        if len(session['urls']) > 4:
            session['urls'].pop(4)
            session['names'].pop(4)
        session.modified = True

"""
Forma auntomática de hacerlo, pero aparecen las url completas y
la carga del icono

@app.after_request
def store_visted_urls(response):
    if 'urls' in session:
        session['urls'].append(request.url)
        session['names'].append(request.url)
        if len(session['urls']) > 3:
            session['urls'].pop(0)
            session['names'].pop(0)
        session.modified = True
    return response
"""
        
# Ejercicio 2: Algoritmos de ordenación

# Ordenación por burbuja
@app.route('/bubblesort/<l>')
def bubbleSort(l):
    l1, t = bubble_sort(l)
    l1 = list(map(str,l1))
    l1 = ', '.join(l1)
    #store_visted_urls(request.url, 'Ej2: Bubble Sort')
    return render_ejer('Bubble Sort',l,l1+'.  '+'Time: '+str(t)+' seconds.')

# Ordenación por selección
@app.route('/selectionsort/<l>')
def selectionSort(l):
    l1, t = selection_sort(l)
    l1 = list(map(str,l1))
    l1 = ', '.join(l1)
    #store_visted_urls(request.url, 'Ej2: Selection Sort')
    return render_ejer('Selection Sort',l,l1+'.  '+'Time: '+str(t)+' seconds.')

# Ordenación por inserción
@app.route('/insertionsort/<l>')
def insertionSort(l):
    l1, t = insertion_sort(l)
    l1 = list(map(str,l1))
    l1 = ', '.join(l1)
    #store_visted_urls(request.url, 'Ej2: Insertion Sort')
    return render_ejer('Insertion Sort',l,l1+'.  '+'Time: '+str(t)+' seconds.')

# Ejercicio 3: Criba de Erastóstenes
@app.route('/erastosthenes/<n>')
def erastosthenes(n):
    #store_visted_urls(request.url, 'Erastosthenes')
    n = int(n)
    if n<0:
        return render_ejer('Criba de Erastóstenes ',str(n),'Incorrect input!')
    
    prime = erastosthenes_sieve(n)
    prime = ', '.join(prime)
    return render_ejer('Criba de Erastóstenes ',str(n),prime)

# Ejercicio 4: Fibonacci
@app.route('/fibonacci/<n>')
def fibonacci(n):
    #store_visted_urls(request.url, 'Fibonacci')
    n = int(n)
    if n<=0:
        return render_ejer('Fibonacci ',str(n),'Incorrect input!')
    
    return render_ejer('Fibonacci ',str(n),str(fibo(n)))

# Ejercicio 5: Corchetes
@app.route('/corchetes/<l>')
def corchetes(l):
    #store_visted_urls(request.url, 'Corchetes')
    return render_ejer('Corchetes', l, brackets(l))

# Ejercicio 6: Expresiones regulares

# Cualquier palabra seguida de un espacio y una única letra mayúscula
@app.route('/re/<cadena>')
def wordCapital(cadena):
    #store_visted_urls(request.url, 'Ej6: Palabra L')
    match = word_capital(cadena)
    return render_ejer('Expresiones regulares: Palabra seguida de espacio y una única letra mayúscula',cadena,', '.join(match))

# Identificar correos electrónicos válidos
@app.route('/emails/<cadena>')
def emails(cadena):
    #store_visted_urls(request.url, 'Ej6: Emails')
    match = e_mails(cadena)
    return render_ejer('Expresiones regulares: Correos electrónicos válidos',cadena,', '.join(match))

# Identificar números de tarjeta de crédito
@app.route('/creditcards/<cadena>')
def creditcards(cadena):
    #store_visted_urls(request.url, 'Ej6: Nºs tarjeta de crédito')
    match = credit_cards(cadena)
    return render_ejer('Expresiones regulares: Números de tarjeta de crédito',cadena,', '.join(match))

# Random SVG
@app.route('/svg')
def random_svg():
    store_visted_urls(request.url, 'SVG')
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
    store_visted_urls(request.url, name)
    return render_template('ejer.html', nombre=name, entrada=inpt, contenido=content)

# Ejercicio 1

@app.route('/adivina', methods=['GET', 'POST'])
def adivina():
    if request.method == 'POST': # Intento
        n=request.form['n']
        if not n:
            return render_template('adivina.html', msg='No introdujiste ningún número.', tries=session['tries'], fin=session['end'])
        n=int(n)
        session['tries']-=1
        if n== session['number']:
            msg='Felicidades! Has ganado!'
            session['end']=True
        elif session['tries']==0:
            msg='Has perdido. Era el '+ str(session['number'])
            session['end']=True
        elif n> session['number']:
            msg='El número buscado es menor.'
        else:
            msg='El número buscado es mayor.'

    else: # Nueva partida
        store_visted_urls(request.url, 'Adivina')
        session['number']=randint(1,100)
        session['tries']=10
        session['end']=False
        msg=''
    return render_template('adivina.html', msg=msg, tries=session['tries'], fin=session['end'])
