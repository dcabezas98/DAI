#./app/app.py

from flask import Flask, render_template, request, flash, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key='esto-es-una-clave-muy-secreta'

client = MongoClient("mongo", 27017) # Conectar al servicio (docker) "mongo" en su puerto estandar
db = client.SampleCollections        # Elegimos la base de datos de ejemplo

# Página principal, con índice
@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def  home():
    return render_template('home.html')

@app.route('/pokemon', methods=['GET','POST'])
def pokemon():    
    if request.method == 'POST':
        if 'name' in request.form:
            pokemons=db.samples_pokemon.find({'name':{"$regex":request.form['name'],"$options":'i'}}).sort('id')
        elif 'num' in request.form:
            n=request.form['num']
            if len(n)<3:
                n='0'*(3-len(n))+n
            pokemons=db.samples_pokemon.find({'num':n}).sort('id')
        elif 'type' in request.form:
            pokemons=db.samples_pokemon.find({'type':{"$regex":request.form['type'],"$options":'i'}}).sort('id')
    else:
        pokemons=db.samples_pokemon.find().sort('id')
        
    lista_pokemons = [{k:p[k] for k in ("num","name","img","type","prev_evolution","next_evolution") if k in p} for p in pokemons]
    
    return render_template('pokemon.html',n=len(lista_pokemons),lista=lista_pokemons)

@app.route('/pokemon/adv', methods=['POST'])
def pokemon_adv():
    
    name=request.form['name']
    typ=request.form['type']
    
    pokemons=db.samples_pokemon.find({'name':{"$regex":request.form['name'],"$options":'i'}, 'type':{"$regex":request.form['type'],"$options":'i'}}).sort('id')
        
    lista_pokemons = [{k:p[k] for k in ("num","name","img","type","prev_evolution","next_evolution") if k in p} for p in pokemons]
    
    return render_template('pokemon.html',n=len(lista_pokemons),lista=lista_pokemons)

# Crea una lista desde un string
def stripList(l):
    l=l.replace('[','').replace(']','').replace(' ','').replace("'","")
    return l.split(',')

# Crea una lista de diccionarios desde un string
def stripDictList(l):
    l=l.replace('[','').replace(']','').replace('{','').replace('}','')
    l=l.replace("'num'",'').replace("'name'",'')
    l=l.replace(' ','').replace(':','').replace("'","")
    l=l.split(',')
    result=[]
    for i in range(0,len(l)-1,2):
        result.append({'num':l[i], 'name':l[i+1]})
    return result

@app.route('/pokemon/edit/<num>', methods=['GET','POST'])
def editPkmn(num):

    if request.method=='POST':
        n=request.form['num']
        if len(n)<3:
                n='0'*(3-len(n))+n
        name=request.form['name']
        img=request.form['img']
        typ=stripList(request.form['type'])
        prev=stripDictList(request.form['prev'])
        nex=stripDictList(request.form['next'])
        # No se puede pisar el número de otro pokemon
        if num==n or db.samples_pokemon.find({'id':int(n)}).count()==0:
            db.samples_pokemon.find_one_and_update({'id':int(num)},
                                                   {'$set':{'name':name,
                                                   'id':int(n), 'img':img,
                                                   'num':n, 'type':typ,
                                                   'prev_evolution':prev,
                                                   'next_evolution':nex}})
            flash('Pokemon data modified successfully.')
            return redirect('/pokemon/edit/'+n)
        else:
            flash('Data not modified. There exists already a Pokemon with such number :(')
        return redirect('/pokemon/edit/'+num)

    pok=db.samples_pokemon.find({'num':num})
    for p in pok:
        pok={k:p[k] for k in ("num","name","img","type","prev_evolution","next_evolution") if k in p}
    
    return render_template('editPkmn.html', pok=pok)

@app.route('/pokemon/add', methods=['GET','POST'])
def addPkmn():
    if request.method=='POST':
        n=request.form['num']
        if len(n)<3:
                n='0'*(3-len(n))+n
        name=request.form['name']
        img=request.form['img']
        typ=stripList(request.form['type'])
        prev=stripDictList(request.form['prev'])
        nex=stripDictList(request.form['next'])
        # No se puede pisar el número de otro pokemon
        if db.samples_pokemon.find({'id':int(n)}).count()==0:
            db.samples_pokemon.insert({'name':name,'id':int(n), 'img':img,
                                                   'num':n, 'type':typ,
                                                   'prev_evolution':prev,
                                                   'next_evolution':nex})
            flash('Pokemon added successfully.')
            return redirect('/pokemon/edit/'+n)
        else:
            flash('Data not modified. There exists already a Pokemon with such number :(')
        
    return render_template('addPkmn.html')


@app.route('/pokemon/delete/<num>')
def deletePkmn(num):
    db.samples_pokemon.delete_one({'num':num})
    flash('Pokemon deleted successfully.')
    return redirect(url_for('home'))
    
# Manejador de error 404: URL no definida
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
