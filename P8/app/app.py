#./app/app.py

from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_restful import Api, Resource, reqparse, abort
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
    return render_template('base.html')

##############
#  API REST  #
##############

@app.route('/api/pokemon', methods=['GET','POST'])
def api_1():

    if request.method == 'GET':
        args=request.args

        name=''
        typ=''

        if 'num' in args and args['num']!='': # Si le pones un número, te devuelve ese número
            n=args['num']
            if len(n)<3:
                n='0'*(3-len(n))+n
            pokemons=db.samples_pokemon.find({'num':n}).sort('id')
        else: # Si no hay número, busca por nombre y tipo
            if 'name' in args:
                name=args['name']
            if 'type' in args:
                typ=args['type']

            pokemons=db.samples_pokemon.find({'name':{"$regex":name,"$options":'i'}, 'type':{"$regex":typ,"$options":'i'}}).sort('id')

        lista_pokemons = [{k:p[k] for k in ("num","name","img","type","prev_evolution","next_evolution") if k in p} for p in pokemons]
        return jsonify(lista_pokemons)

    if request.method == 'POST':
        args=request.json

        n=args['num']
        if len(n)<3:
            n='0'*(3-len(n))+n
        args['num']=n
        if db.samples_pokemon.find({'id':int(n)}).count()==0:
            args['id']=int(n)
            db.samples_pokemon.insert(args)
            del args['_id']
            return jsonify(args)

        else:
            return jsonify({'error':'A Pokemon with such number already exists'})

@app.route('/api/pokemon/<id>', methods=['GET','PUT','DELETE'])
def api_2(id):

    if request.method == 'GET':
        try:
            pkmn = db.samples_pokemon.find_one({'id': int(id)})
            pkmn={k:pkmn[k] for k in ("num","name","img","type","prev_evolution","next_evolution") if k in pkmn}
            pkmn['id']=int(id)
            return jsonify(pkmn)
        except:
            return jsonify({'error':'Not found'}), 404

    if request.method == 'DELETE':
        if db.samples_pokemon.find({'id':int(id)}).count()==0:
            return jsonify({'error':'Not found'}), 404
        db.samples_pokemon.delete_one({'id':int(id)})
        return jsonify({'id':int(id)})

    if request.method == 'PUT':
        if db.samples_pokemon.find({'id':int(id)}).count()==0:
            return jsonify({'error':'Not found'}), 404
        args=request.json
        n=id
        if 'num' in args:
            n=int(args['num'])
            if n != int(id) and db.samples_pokemon.find({'id':n}).count()>0:
                return jsonify({'error':'A Pokemon with such id already exists'})
            args['id']=n
        db.samples_pokemon.find_one_and_update({'id':int(id)},{'$set':args})
        id=n
        return redirect('/api/pokemon/'+str(id))   

#################################
#  API REST CON FLASK-RESTFULL  #
#################################

api = Api(app)

pokemon_get_args=reqparse.RequestParser()
pokemon_get_args.add_argument("name", type=str)
pokemon_get_args.add_argument("type", type=str)
pokemon_get_args.add_argument("num", type=str)

class Pkmns(Resource):

    def get(self):
        args=pokemon_get_args.parse_args()
        #args=request.args
        name=''
        typ=''

        if args['num']!=None and args['num']!='': # Si le pones un número, te devuelve ese número
            n=args['num']
            if len(n)<3:
                n='0'*(3-len(n))+n
            pokemons=db.samples_pokemon.find({'num':n}).sort('id')
        else: # Si no hay número, busca por nombre y tipo
            if args['name']!=None:
                name=args['name']
            if args['type']!=None:
                typ=args['type']

            pokemons=db.samples_pokemon.find({'name':{"$regex":name,"$options":'i'}, 'type':{"$regex":typ,"$options":'i'}}).sort('id')

        lista_pokemons = [{k:p[k] for k in ("num","name","img","type","prev_evolution","next_evolution") if k in p} for p in pokemons]
        return jsonify(lista_pokemons)

    def post(self):
        args=request.json

        n=args['num']
        if len(n)<3:
            n='0'*(3-len(n))+n
        args['num']=n
        if db.samples_pokemon.find({'id':int(n)}).count()==0:
            args['id']=int(n)
            db.samples_pokemon.insert(args)
            del args['_id']
            return jsonify(args)

        else:
            return jsonify({'error':'A Pokemon with such number already exists'})

class Pkmn(Resource):

    def get(self, id):
        try:
            pkmn = db.samples_pokemon.find_one({'id': int(id)})
            pkmn={k:pkmn[k] for k in ("num","name","img","type","prev_evolution","next_evolution") if k in pkmn}
            pkmn['id']=int(id)
            return jsonify(pkmn)
        except:
            return {'error':'Not found'}, 404

    def delete(self, id):
        if db.samples_pokemon.find({'id':int(id)}).count()==0:
            return {'error':'Not found'}, 404
        db.samples_pokemon.delete_one({'id':int(id)})
        return jsonify({'id':int(id)})

    def put(self, id):
        if db.samples_pokemon.find({'id':int(id)}).count()==0:
            return {'error':'Not found'}, 404
        args=request.json
        n=id
        if 'num' in args:
            n=int(args['num'])
            if n != int(id) and db.samples_pokemon.find({'id':n}).count()>0:
                return jsonify({'error':'A Pokemon with such id already exists'})
            args['id']=n
        db.samples_pokemon.find_one_and_update({'id':int(id)},{'$set':args})
        id=n
        return redirect('/api/pokemon/'+str(id))

api.add_resource(Pkmn, "/api2/pokemon/<id>")
api.add_resource(Pkmns, "/api2/pokemon")
