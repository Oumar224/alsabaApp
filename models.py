import os
from config import database_path
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate



db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app):
    app.config.from_object('config')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    db.app = app
    migrate=Migrate(app , db)
    db.init_app(app)
   



"""
Agence

"""
class Agence(db.Model):
    __tablename__ = 'agences'

    agenceId = db.Column(db.Integer, primary_key=True)
    nomAgence = db.Column(db.String(120) , nullable=False)
    emailAgence = db.Column(db.String(120) , nullable=False)
    motDePasse= db.Column(db.String(200), nullable=False)
    phone=db.Column(db.String(120) , nullable=False)
    responsable=db.Column(db.String(120) , nullable=False)
    agence_caisse = db.relationship('AgenceCaisse', cascade="all, delete" ,  backref=db.backref('agence') , lazy='select' )
    agence_fond = db.relationship('AgenceFond', cascade="all, delete" ,  backref=db.backref('agence') , lazy='select')
    agencePlanification = db.relationship('AgencePlanification', cascade="all, delete" ,  backref=db.backref('agence') , lazy='select')
    agence_transation= db.relationship('AgenceTransation', cascade="all, delete" ,  backref=db.backref('agence') , lazy='select')
    agence_bilan= db.relationship('AgenceBilan', cascade="all, delete" ,  backref=db.backref('agence') , lazy='select')


    def __init__(self, nomAgence, phone , responsable , emailAgence , motDePasse):
        self.nomAgence = nomAgence
        self.phone = phone
        self.responsable = responsable
        self.emailAgence = emailAgence
        self.motDePasse = motDePasse

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



    def format(self):
        return {
            'id': self.agenceId,
            'nomAgence': self.nomAgence,
            'phone': self.phone,
            'responsable': self.responsable,
            }


"""
AgenceCaisse

"""
class AgenceCaisse(db.Model):
    __tablename__ = 'agence_caisses'

    agenceCaisseId = db.Column(db.Integer, primary_key=True)
    initial = db.Column(db.Float(precision=2) , nullable=False)
    entree = db.Column(db.Float(precision=2) , nullable=False)
    sortie = db.Column(db.Float(precision=2) , nullable=False)
    disponibilitee = db.Column(db.Float(precision=2) , nullable=False)
    date = db.Column(db.DateTime , nullable=False)
    agence_id = db.Column(db.Integer, db.ForeignKey('agences.agenceId'), nullable=False)

    def __init__(self, initial, entree, sortie, disponibilitee ,date ,  agence_id ):
        self.initial = initial
        self.entree = entree
        self.sortie = sortie
        self.disponibilitee = disponibilitee
        self.date = date
        self. agence_id =  agence_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.agenceCaisseId,
            'initial': self.initial,
            'entree': self.entree,
            'sortie': self.sortie,
            'disponibilitee': self.disponibilitee,
            'date': self.date,
            'agence_id': self. agence_id
            }



"""
AgenceFond

"""
class AgenceFond(db.Model):
    __tablename__ = 'agence_fonds'

    agenceFondId = db.Column(db.Integer, primary_key=True)
    typeFond = db.Column(db.Float(precision=2) , nullable=False)
    fondDate = db.Column(db.DateTime , nullable=False)
    montant = db.Column(db.Float(precision=2) , nullable=False)
    operande = db.Column(db.String(3000) , nullable=False)
    agence_id = db.Column(db.Integer, db.ForeignKey('agences.agenceId'), nullable=False)

    def __init__(self, typeFond, fondDate, montant, operande , agence_id ):
        self.typeFond = typeFond
        self.fondDate = fondDate
        self.montant = montant
        self.operande = operande
        self.agence_id = agence_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.agenceFondId,
            'typeFond': self.typeFond,
            'fondDate': self.fondDate,
            'montant': self.montant,
            'operande': self.operande,
            'agence_id': self.agence_id
            }


"""
AgencePlanification

"""
class AgencePlanification(db.Model):
    __tablename__ = 'agence_planification'

    agencePlanificationId = db.Column(db.Integer, primary_key=True)
    intituleTache = db.Column(db.String(300) , nullable=False)
    tacheDate = db.Column(db.DateTime , nullable=False)
    status = db.Column(db.Boolean , nullable=False)
    agence_id = db.Column(db.Integer, db.ForeignKey('agences.agenceId'), nullable=False)

    def __init__(self, intituleTache, tacheDate, status , agence_id ):
        self.intituleTache = intituleTache
        self.tacheDate = tacheDate
        self.status = status
        self. agence_id =  agence_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.agencePlanificationId,
            'status': self.status,
            'tacheDate': self.tacheDate,
            'intituleTache': self.intituleTache,
            'agence_id': self. agence_id
            }




"""
AgenceTransation

"""
class AgenceTransation(db.Model):
    __tablename__ = 'agence_transactions'

    agenceTransationId = db.Column(db.Integer, primary_key=True)
    mal = db.Column(db.Float(precision=2) , nullable=False)
    fac = db.Column(db.Float(precision=2) , nullable=False)
    fom = db.Column(db.Float(precision=2) , nullable=False)
    code = db.Column(db.String(120) , nullable=False)
    telDest = db.Column(db.String(120) , nullable=False)
    telExp = db.Column(db.String(120) , nullable=False)
    nomDest = db.Column(db.String(120) , nullable=False)
    nomExp = db.Column(db.String(120) , nullable=False)
    typeTrans= db.Column(db.String(200) , nullable=False)
    dateTrans= db.Column(db.DateTime , nullable=False)
    villeDest= db.Column(db.String(200) , nullable=False)
    agence_dest = db.Column(db.String(180), nullable=False)
    agence_exp = db.Column(db.Integer, db.ForeignKey('agences.agenceId'), nullable=False)

    def __init__(self, mal, fac , fom , code , telDest , telExp ,nomDest ,nomExp ,typeTrans , dateTrans , villeDest  , agence_dest ,  agence_exp):
        self.mal = mal
        self.fac = fac
        self.fom = fom
        self.code = code
        self.telDest = telDest
        self.telExp = telExp
        self.nomDest = nomDest
        self.nomExp = nomExp
        self.typeTrans = typeTrans
        self.dateTrans = dateTrans
        self.villeDest = villeDest
        self.agence_dest = agence_dest
        self.agence_exp = agence_exp

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def roolback(self):
        db.session.rollback()
    
    def close_session(self):
         db.session.close()



    def format(self):
        return {
            'id': self.agenceTransationId,
            'mal': self.mal,
            'fac': self.fac,
            'fom': self.fom,
            'code': self.code,
            'telDest': self.telDest,
            'telExp': self.telExp,
            'nomDest': self.nomDest,
            'nomExp': self.nomExp,
            'typeTrans': self.typeTrans,
            'dateTrans': self.dateTrans,
            'villeDest': self.villeDest,
            'agenceDest': self.agence_dest,
            'agenceExp':self.agence_exp
            }



"""
AgenceBilan

"""
class AgenceBilan(db.Model):
    __tablename__ = 'agence_bilans'

    AgenceBilanId = db.Column(db.Integer, primary_key=True)
    epargne = db.Column(db.Float(precision=2) , nullable=False)
    prets = db.Column(db.Float(precision=2) , nullable=False)
    initial = db.Column(db.Float(precision=2) , nullable=False)
    emprunts = db.Column(db.Float(precision=2) , nullable=False)
    injections = db.Column(db.Float(precision=2) , nullable=False)
    entrees = db.Column(db.Float(precision=2) , nullable=False)
    sorties = db.Column(db.Float(precision=2) , nullable=False)
    soldes = db.Column(db.Float(precision=2) , nullable=False)
    chargeFictives= db.Column(db.Float(precision=2) , nullable=False)
    chargeReelles= db.Column(db.Float(precision=2) , nullable=False)
    disponibilitee= db.Column(db.Float(precision=2) , nullable=False)
    dettes = db.Column(db.Float(precision=2) , nullable=False)
    date_bilan=db.Column(db.DateTime , nullable=False)
    agence_id = db.Column(db.Integer, db.ForeignKey('agences.agenceId'), nullable=False)

    def __init__(self, epargne, prets , initial , emprunts , injections , entrees ,sorties , chargeFictives ,chargeReelles , disponibilitee , dettes  , agence_id , date_bilan):
        self.epargne = epargne
        self.prets = prets
        self.initial = initial
        self.emprunts = emprunts
        self.injections = injections
        self.entrees = entrees
        self.sorties = sorties
        self.chargeFictives = chargeFictives
        self.chargeReelles = chargeReelles
        self.disponibilitee = disponibilitee
        self.dettes = dettes
        self.date_bilan = date_bilan
        self.agence_id = agence_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def roolback(self):
        db.session.rollback()
    
    def close_session(self):
         db.session.close()



    def format(self):
        return {
            'id': self.AgenceBilanId,
            'epargne': self.epargne,
            'prets': self.prets,
            'initial': self.initial,
            'emprunts': self.emprunts,
            'injections': self.injections,
            'entrees': self.entrees,
            'sorties': self.sorties,
            'chargeFictives': self.chargeFictives,
            'chargeReelles': self.chargeReelles,
            'disponibilitee': self.disponibilitee,
            'dettes': self.dettes,
            'date': self.date_bilan,
            'agence_id': self.agence_id
            }
