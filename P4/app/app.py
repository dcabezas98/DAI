#./app/app.py

from flask import Flask, render_template, session, request, flash, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongo", 27017) # Conectar al servicio (docker) "mongo" en su puerto estandar
db = client.SampleCollections        # Elegimos la base de datos de ejemplo

@app.route('/home')
def  home():
    return render_template('home.html')

@app.route('/pokemon', methods=['GET','POST'])
def pokemon():
    pokemons=db.samples_pokemon.find()
    
    if request.method == 'POST':
        if 'name' in request.form:
            pokemons=db.samples_pokemon.find({'name':request.form['name']})
        elif 'num' in request.form:
            n=request.form['num']
            pokemons=db.samples_pokemon.find({'num':'0'*(3-len(n))+request.form['num']})
        elif 'type' in request.form:
            pokemons=db.samples_pokemon.find({'type':request.form['type']})
    else:
        pokemons=db.samples_pokemon.find()
        
    lista_pokemons = [{k:p[k] for k in ("num","name","img","type","prev_evolution","next_evolution") if k in p} for p in pokemons]
    
    return render_template('pokemon.html',lista=lista_pokemons)

# Manejador de error 404: URL no definida
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
