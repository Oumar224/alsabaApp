# from crypt import request.method 
import json
import random
import string
import os
from datetime import date, datetime
import string
from tokenize import String
from urllib import response
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


DATA_PER_PAGE=4 

from models import setup_db, AgenceTransation, AgencePlanification, AgenceFond , AgenceCaisse , Agence

def paginate_method(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * DATA_PER_PAGE
    end = start + DATA_PER_PAGE
    selections = [data.format() for data in selection]
    current_plants = selections[start:end]
    return current_plants

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
     Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors=CORS(app , resources={r"api/*":{"origins":"*"}})


    """
     Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Acess-Control-Allow-Headers' , 'Content-Type , Authorization')
        response.headers.add('Acess-Control-Allow-Methods' , 'GET , POST , DELETE , PUT ,PATCH , OPTIONS')
        return response


    """                             HERE IS THE CRUD FOR EACH RESSOURCES                        """

    """
    transactions
    """
    #adding

    @app.route("/altaba/transactions" , methods=['POST' , 'GET'])
    def handle_transactions_getting():
        # insert new data
        if request.method =='POST':
            characters = string.ascii_letters + string.digits
            body = request.get_json() 
            if body.get('mal', None) is None or body.get('fac', None) is None:
                abort(404)
            else :
                try:
                    data=json.dumps(body.get('dateTrans') , indent = 4)
                    data = json.loads(data)
                    transaction=AgenceTransation(
                    mal= body.get('mal', None),
                    fac = body.get('fac', None),
                    fom = body.get('fom', None),
                    code = ''.join(random.choice(characters) for i in range(12)).upper(),
                    telDest = body.get('telDest', None),
                    telExp = body.get('telExp', None),
                    nomDest = body.get('nomDest', None),
                    nomExp = body.get('nomExp', None),
                    typeTrans = body.get('typeTrans', None),
                    dateTrans = datetime(data['annee'] , data['mois'] , data['jour']['valeur'] , data['jour']['heure'] , data['jour']['minute'] , data['jour']['second'] ),
                    villeDest = body.get('villeDest', None),
                    agence_dest= body.get('agence_dest', None),
                    agence_exp= body.get('agence_exp', None))
                    transaction.insert()
                    return jsonify (
                    { "Succes":True,
                        "Transaction":transaction.format() , 
                        "TotalTransaction":len(AgenceTransation.query.all())
                        }
                    )
                except:
                    abort(500)
        
        # get all  data
        elif request.method =='GET':
            transaction=AgenceTransation.query.all()
            current_transaction = paginate_method(request, transaction)
            if len(current_transaction) == 0:
                abort(404)
            else:
                try:
                    return jsonify({
                        'Success': True,
                        'Transaction': current_transaction,
                        'TotalTransactions': len(transaction)
                    })
                except :
                    abort(422)
        else:
            abort(405)


    #retrievement
    @app.route("/altaba/transactions/<int:transaction_id>" , methods=['PATCH' , 'DELETE'])
    def handle_transactions_retrieve(transaction_id):
        method = request.args.get('method_value','')
    
        # partial update of specifique data
        if request.method  =='PATCH' and method=='update' :
            body = request.get_json()
            transaction = AgenceTransation.query.filter_by(agenceTransationId=transaction_id).one_or_none()
            if transaction is None:
                abort(404)
            else:
                try:
                    if 'mal' in body :
                        transaction.mal = body.get('mal')
                    if 'fac' in body : 
                        transaction.fac = body.get('fac')
                    if 'fom' in body :
                        transaction.fom = body.get('fom')
                    if 'code' in body: 
                        transaction.code = body.get('code')
                    if 'telDest' in body :
                        transaction.telDest = body.get('telDest')
                    if 'telExp' in body :
                        transaction.telExp = body.get('telExp')
                    if  'nomDest' in body :
                        transaction.nomDest = body.get('nomDest')
                    if  'nomExp' in body  :
                        transaction.nomExp = body.get('nomExp')
                    if 'typeTrans' in body:
                        transaction.typeTrans = body.get('typeTrans')
                    if 'dateTrans' in body:
                        data=json.dumps(body.get('dateTrans') , indent = 4)
                        data = json.loads(data)
                        transaction.dateTrans = datetime(data['annee'] , data['mois'] , data['jour']['valeur'] , data['jour']['heure'] , data['jour']['minute'] , data['jour']['second'] )
                    if 'villeDest' in body:
                        transaction.villeDest = body.get('villeDest')
                    if 'agence_dest' in body :
                        transaction.agence_dest = body.get('agence_dest')
                    if 'agence_exp' in body : 
                        transaction.agence_exp = body.get('agence_exp')
                    transaction.update()
                    return jsonify({
                        'success': True,
                        'Transaction': transaction.format()
                    })
                except:
                    abort(500)
        
        # delete a specifique  data
        elif request.method =='DELETE' and method=='delete':
            transaction = AgenceTransation.query.filter_by(agenceTransationId=transaction_id).one_or_none()
            if transaction is None:
                abort(404)
            else:
                try:
                    transaction.delete()
                    totals_transactions = transaction.query.all()
                    return jsonify({
                        'success': True,
                        'deleted': transaction_id,
                        'Transaction': paginate_method(request, totals_transactions),
                        'totalTransactions': len(totals_transactions)
                    })
                except:
                    abort(422)
        else:
            abort(405)



    """
    Agence
    """

    #adding 

    @app.route("/altaba/agences" , methods=['POST' , 'GET'])
    def handle_agences_getting():
        # insert new data
        if request.method =='POST':
            body = request.get_json() 
            if body.get('nomAgence', None) is None or body.get('emailAgence', None) is None:
                abort(404)
            else :
                try:
                    agence=Agence(
                    nomAgence= body.get('nomAgence', None),
                    emailAgence = body.get('emailAgence', None),
                    motDePasse = body.get('motDePasse', None),
                    phone = body.get('phone', None),
                    responsable = body.get('responsable', None))
                    agence.insert()
                    return jsonify (
                    { "Succes":True,
                        "Agence":agence.format() , 
                        "TotalAgences":len(Agence.query.all())
                    }
                    )
                except:
                    abort(500)
        
        # get all  data
        elif request.method =='GET':
            agence=Agence.query.all()
            current_agence = paginate_method(request, agence)
            if len(current_agence) == 0:
                abort(404)
            else:
                try:
                    return jsonify({
                        'Success': True,
                        'Agence': current_agence,
                        'TotalAgences': len(agence)
                    })
                except :
                    abort(422)
        else:
            abort(405)

    #retrievement

    @app.route("/altaba/agences/<int:agence_id>" , methods=['PATCH' , 'DELETE'])
    def handle_agences_retrieve(agence_id):
        method = request.args.get('method_value','')
        # partial update of specifique data
        if request.method  =='PATCH' and method=='update' :
            body = request.get_json()
            agence = Agence.query.filter_by(agenceId=agence_id).one_or_none()
            if agence is None:
                abort(404)
            else:
                try:
                    if 'nomAgence' in body :
                        agence.nomAgence = body.get('nomAgence')
                    if 'emailAgence' in body : 
                        agence.emailAgence = body.get('emailAgence')
                    if 'motDePasse' in body :
                        agence.motDePasse = body.get('motDePasse')
                    if 'phone' in body: 
                        agence.phone = body.get('phone')
                    if 'responsable' in body :
                        agence.responsable = body.get('responsable')
                    agence.update()
                    return jsonify({
                        'success': True,
                        'Agence': agence.format()
                    })
                except:
                    abort(500)
        
        # delete a specifique  data
        elif request.method =='DELETE' and method=='delete':
            agence = Agence.query.filter_by(agenceId=agence_id).one_or_none()
            if agence is None:
                abort(404)
            else:
                try:
                    agence.delete()
                    totals_agence = agence.query.all()
                    return jsonify({
                        'Success': True,
                        'Deleted': agence_id,
                        'Agence': paginate_method(request, totals_agence),
                        'TotalAgences': len(totals_agence)
                    })
                except:
                    abort(422)
        else:
            abort(405)

    """
   AgenceFond
    """

    #adding 

    @app.route("/altaba/fonds" , methods=['POST' , 'GET'])
    def handle_fonds_getting():
        # insert new data
        if request.method =='POST':
            body = request.get_json() 
            if body.get('typeFond', None) is None or body.get('operande', None) is None:
                abort(404)
            else :
                try :
                    data=json.dumps(body.get('dateTrans') , indent = 4)
                    data = json.loads(data)
                    fond=AgenceFond(
                    typeFond = body.get('typeFond', None),
                    fondDate = datetime(data['annee'] , data['mois'] , data['jour']['valeur'] , data['jour']['heure'] , data['jour']['minute'] , data['jour']['second'] ),
                    montant = body.get('montant', None),
                    operande = body.get('operande', None),
                    agence_id = body.get('agence_id', None))
                    fond.insert()
                    return jsonify (
                    { "succes":True,
                        "Fond":fond.format() , 
                        "TotalFonds":len(AgenceFond.query.all())
                    }
                    )
                except :
                    abort(500)
        
        # get all  data
        elif request.method =='GET':
            fond=AgenceFond.query.all()
            current_fonds = paginate_method(request, fond)
            if len(current_fonds) == 0:
                abort(404)
            else:
                try :
                    return jsonify({
                        'Success': True,
                        'Fond': current_fonds,
                        'TotalFonds': len(fond)
                    })
                except:
                    abort(422)
        else:
            abort(405)
    

    #retrivement

    @app.route("/altaba/fonds/<int:fond_id>" , methods=['PATCH' , 'DELETE'])
    def handle_fonds_retrieve(fond_id):
        method = request.args.get('method_value','')
        # partial update of specifique data
        if request.method  =='PATCH' and method=='update' :
            body = request.get_json()
            fond= AgenceFond.query.filter_by(agenceFondId=fond_id).one_or_none()
            if fond is None:
                abort(404)
            else:
                try:
                    if 'typeFond' in body :
                        fond.typeFond = body.get('typeFond')
                    if 'montant' in body : 
                        fond.montant = body.get('montant')
                    if 'operande' in body :
                        fond.operande = body.get('operande')
                    if 'agence_id' in body: 
                        fond.agence_id = body.get('agence_id')
                        data = json.loads(body.get('fondDate'))
                    if 'fondDate' in body :
                        data=json.dumps(body.get('dateTrans') , indent = 4)
                        data = json.loads(data)
                        fond.fondDate= datetime(data['annee'] , data['mois'] , data['jour']['valeur'] , data['jour']['heure'] , data['jour']['minute'] , data['jour']['second'] )
                    fond.update()
                    return jsonify({
                        'Success': True,
                        'Fond': fond.format()
                    })
                except:
                    abort(500)
        
        # delete a specifique  data
        elif request.method =='DELETE' and method=='delete':
            fond = AgenceFond.query.filter_by(agenceFondId=fond_id).one_or_none()
            if fond is None:
                abort(404)
            else:
                try:
                    fond.delete()
                    totals_fond = fond.query.all()
                    return jsonify({
                        'Success': True,
                        'Deleted': fond_id,
                        'Fond': paginate_method(request, totals_fond),
                        'TotalFond': len(totals_fond)
                    })
                except:
                    abort(422)
        else:
            abort(405)
       




    """
    AgenceCaisse
    """

#adding 

    @app.route("/altaba/caisses" , methods=['POST' , 'GET'])
    def handle_caisses_getting():
        # insert new data
        if request.method =='POST':
            body = request.get_json() 
            if body.get('initial', None) is None or body.get('entree', None) is None:
                abort(404)
            else :
                try:
                    data=json.dumps(body.get('dateTrans') , indent = 4)
                    data = json.loads(data)
                    caisse=AgenceCaisse(
                    initial= body.get('initial', None),
                    date =  datetime(data['annee'] , data['mois'] , data['jour']['valeur'] , data['jour']['heure'] , data['jour']['minute'] , data['jour']['second'] ),
                    entree = body.get('entree', None),
                    sortie = body.get('sortie', None),
                    disponibilitee = body.get('disponibilitee', None),
                    agence_id = body.get('agence_id', None))
                    caisse.insert()
                    return jsonify (
                    { "Succes":True,
                        "Caisse":caisse.format() , 
                        "TotalCaisses":len(AgenceCaisse.query.all())
                    }
                    )
                except:
                    abort(500)
        
        # get all  data
        elif request.method =='GET':
            caisse=AgenceCaisse.query.all()
            if len(caisse) == 0:
                abort(404)
            else:
                try:
                    current_caisse = paginate_method(request, caisse)
                    return jsonify({
                        'Success': True,
                        'Caisse': current_caisse,
                        'TotalCaisse': len(caisse)
                    })
                except :
                    abort(422)
        else:
            abort(405)

    #retrievement

    @app.route("/altaba/caisses/<int:caisse_id>" , methods=['PATCH' , 'DELETE'])
    def handle_caisses_retrieve(caisse_id):
        method = request.args.get('method_value','') 
        # partial update of specifique data
        if request.method  =='PATCH' and method=='update' :
            body = request.get_json()
            caisse = AgenceCaisse.query.filter_by(agenceCaisseId=caisse_id).one_or_none()
            if caisse is None:
                abort(404)
            else:
                try:
                    if 'initial' in body :
                        caisse.initial = body.get('initial')
                    if 'entree' in body : 
                        caisse.entree = body.get('entree')
                    if 'sortie' in body :
                        caisse.sortie = body.get('sortie')
                    if 'disponibilitee' in body: 
                        caisse.disponibilitee = body.get('disponibilitee')
                    if 'date' in body :
                        data=json.dumps(body.get('dateTrans') , indent = 4)
                        data = json.loads(data)
                        caisse.date= datetime(data['annee'] , data['mois'] , data['jour']['valeur'] , data['jour']['heure'] , data['jour']['minute'] , data['jour']['second'] )
                    if 'agence_id' in body :
                        caisse.agence_id = body.get('agence_id')
                    caisse.update()
                    return jsonify({
                        'Success': True,
                        'Caisse': caisse.format()
                    })
                except:
                    abort(500)
        
        # delete a specifique  data
        elif request.method =='DELETE' and method=='delete':
            caisse = AgenceCaisse.query.filter_by(agenceCaisseId=caisse_id).one_or_none()
            if caisse is None:
                abort(404)
            else:
                try:
                    caisse.delete()
                    totals_caisse = AgenceCaisse.query.all()
                    return jsonify({
                        'Success': True,
                        'Deleted': caisse_id,
                        'Caisse': paginate_method(request, totals_caisse),
                        'TotalCaisse': len(totals_caisse)
                    })
                except:
                    abort(422)
        else:
            abort(405)




    """
    AgencePlanification
    """

#adding 

    @app.route("/altaba/planifications" , methods=['POST' , 'GET'])
    def handle_planifications_getting():
        # insert new data
        if request.method =='POST':
            body = request.get_json() 
            if body.get('intituleTache', None) is None or body.get('agence_id', None) is None:
                abort(404)
            else :
                try:
                    data=json.dumps(body.get('tacheDate') , indent = 4)
                    data = json.loads(data)
                    planification=AgencePlanification(
                    intituleTache= body.get('intituleTache', None),
                    tacheDate =  datetime(data['annee'] , data['mois'] , data['jour']['valeur'] , data['jour']['heure'] , data['jour']['minute'] , data['jour']['second'] ),
                    status = body.get('status', None),
                    agence_id = body.get('agence_id', None))
                    planification.insert()
                    return jsonify (
                    { "Succes":True,
                        "Planification":planification.format() , 
                        "TotalPlanifications":len(AgencePlanification.query.all())
                    }
                    )
                except:
                    abort(500)
        
        # get all  data
        elif request.method =='GET':
            planification=AgencePlanification.query.all()
            if len(planification) == 0:
                abort(404)
            else:
                try:
                    current_planification = paginate_method(request, planification)
                    return jsonify({
                        'Success': True,
                        'Planification': current_planification,
                        'TotalPlanifications': len(planification)
                    })
                except :
                    abort(422)
        else:
            abort(405)

    #retrievement

    @app.route("/altaba/planifications/<int:planification_id>" , methods=['PATCH' , 'DELETE'])
    def handle_planifications_retrieve(planification_id):
        method = request.args.get('method_value','') 
        # partial update of specifique data
        if request.method  =='PATCH' and method=='update' :
            body = request.get_json()
            planification = AgencePlanification.query.filter_by(agencePlanificationId=planification_id).one_or_none()
            if planification is None:
                abort(404)
            else:
                try:
                    if 'intituleTache' in body :
                        planification.intituleTache = body.get('intituleTache')
                    if 'status' in body : 
                        planification.status = body.get('status')
                    if 'tacheDate' in body :
                        planification.tacheDate = body.get('tacheDate')
                    if 'agence_id' in body :
                        planification.agence_id = body.get('agence_id')
                    planification.update()
                    return jsonify({
                        'Success': True,
                        'planification': planification.format()
                    })
                except:
                    abort(500)
        
        # delete a specifique  data
        elif request.method =='DELETE' and method=='delete':
            planification = AgencePlanification.query.filter_by(agencePlanificationId=planification_id).one_or_none()
            if planification is None:
                abort(404)
            else:
                try:
                    planification.delete()
                    totals_planification = AgencePlanification.query.all()
                    return jsonify({
                        'Success': True,
                        'Deleted': planification_id,
                        'Planification': paginate_method(request, totals_planification),
                        'TotalPlanifications': len(totals_planification)
                    })
                except:
                    abort(422)
        else:
            abort(405)


    """                             HERE IS THE BUSINESS MODELS ENDPOINTS                      """

    """
    ALL ABOUT THE TRANSACTIONS
    """
    @app.route("/altaba/agences/roulements")
    def get_transactions():
        nom_agence_dest = request.args.get('agence_dest','' , string)
        nom_agence_exp = request.args.get('agence_exp','' , string)
        agence_exp= Agence.query.filter_by(nomAgence=nom_agence_exp).one_or_none()
        agence_dest= Agence.query.filter_by(nomAgence=nom_agence_dest).one_or_none()
        #get agence exp id
        agence_exp_id=agence_exp[0].agenceId

        # transactions_exp=AgenceTransation.query.filter_by(agence_exp=agence)
        # transactions_dest=AgenceTransation.query.filter_by(agence_exp=agence)
        # fonds=AgenceFond.query.all()
        if len(agence_exp)==0 or len(agence_dest)==0:
            abort(404)
        else:
            return jsonify([{
                'Success': True,
                'Date': trans_date,
                # 'Epargne': len(caisse),
                # 'Prets': len(caisse),
                # 'Agence_exp':agence,
                # 'Agence_dest':'value',
                # 'Initial': AgenceTransation.query.filter_by(agence_id=agence),
                # 'Emprunts': len(caisse),
                # 'Injections': len(caisse),
                'Entrees':AgenceTransation.query.filter(AgenceTransation.agence_exp==agence_exp_id , func.date(AgenceTransation.dateTrans)==trans_date).query.with_entities(func.sum(AgenceTransation.query.filter_by((AgenceTransation.agence_exp==agence_exp_id , func.date(AgenceTransation.dateTrans)==trans_date) ).mal  +   AgenceTransation.query.filter_by((AgenceTransation.agence_exp==agence_exp_id , func.date(AgenceTransation.dateTrans)==trans_date) ).fac +  AgenceTransation.query.filter_by((AgenceTransation.agence_exp==agence_exp_id , func.date(AgenceTransation.dateTrans)==trans_date) ).fom ).label('entrees')).first().total,
                # 'Sorties':AgenceTransation.query.filter(AgenceTransation.agence_dest==nom_agence_dest).query.with_entities(func.sum(agence_trans.mal).label('sorties')).first().total,
                # 'Solde': len(caisse),
                # 'Charges_fictives': len(caisse),
                # 'Charges_reelles': len(caisse),
                # 'Disponibilitee': len(caisse),
                # 'Dettes': len(caisse),
                # 'agence': len(caisse),
            } for trans_date in AgenceTransation.query.with_entities(func.date(AgenceTransation.dateTrans)).distinct().all()] )
    """
   
    """

    """
  
    """

    """
   
    """

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({'success': False, 'error': 404,
                'message': 'Not found'}), 404)

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({'success': False, 'error': 422,
                'message': 'unprocessable'}), 422)

    @app.errorhandler(400)
    def error_client(error):
        return (jsonify({'success': False, 'error': 400,
                'message': 'Bad request'}), 400)

    @app.errorhandler(500)
    def server_error(error):
        return (jsonify({'success': False, 'error': 500,
                'message': 'internal server error'}), 500)

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (jsonify({'success': False, 'error': 405,
                'message': 'method not allowed'}), 405)


    @app.errorhandler(401)
    def unauthorized(error):
        return (jsonify({'success': False, 'error': 401,
                'message': 'unauthorized'}), 401)




    return app

