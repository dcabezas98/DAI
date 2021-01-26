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

# Página de estadísticas: Número de Pokemon de cada tipo
@app.route('/stats-type')
def statsType():
    data={}
    types=db.samples_pokemon.distinct("type") # Lista de tipos
    for t in types:
        data[t]=db.samples_pokemon.find({"type":t}).count() # Número de Pokemon de cada tipo
    return render_template('stats-type.html', types=list(data.keys()), counts=list(data.values()))

# Página de estadísticas: Proporción de Pokemon en cada etapa de evolución
@app.route('/stats-evol')
def statsEvol():
    count=[0]*3
    count[1]=db.samples_pokemon.find({"prev_evolution":{ "$exists": True, "$size": 1}}).count() # Han evolucionado una vez
    count[2]=db.samples_pokemon.find({"prev_evolution":{ "$exists": True, "$size": 2}}).count() # Han evolucionado dos veces
    count[0]=db.samples_pokemon.find({"prev_evolution":{ "$exists": False}}).count() # No han evolucionado nunca
    count[0]+=db.samples_pokemon.find({"prev_evolution":{ "$exists": True, "$size": 0}}).count()
    return render_template('stats-evol.html', count=count)

# Mapas interactivos
@app.route('/map-markers')
def mapMarkers():
    return render_template('map-markers.html')

@app.route('/map-explore')
def mapExplore():
    return render_template('map-explore.html')

##############
#  API REST  #
##############

@app.route('/api/pokemon', methods=['GET','POST'])
def api_1():

    if request.method == 'GET':
        args=request.args

        name=''
        typ=''

        if 'num' in args: # Si le pones un número, te devuelve ese número
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

        if args['num']!=None: # Si le pones un número, te devuelve ese número
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
