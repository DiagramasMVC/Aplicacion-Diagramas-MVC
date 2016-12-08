# -*- coding: utf-8 -*-.

# DESCRIPCION: Definicion del modelo de datos y funciones utiles para manejar
#              la base de datos.


#################################################################################
# # Se importan las librerias necesarias.
# import sys

# from flask import json

# sys.path.append('../../')
# from app import db
#################################################################################

# Se importan las librerias necesarias.
import os
import datetime

from flask                 import Flask
from flask.ext.migrate     import Migrate, MigrateCommand
from flask.ext.sqlalchemy  import SQLAlchemy
from flask.ext.script      import Manager

from sqlalchemy import *

# Conexion con la base de datos.
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'apl.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Instancia de la aplicacion.
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']  = True

# Instancia de la base de datos.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


    #############################################
    #          Definicion del Esquema           #
    #############################################

class clsUsuario(db.Model):
    '''Esquema de la tabla de usuarios.'''

    __tablename__    = 'usuario'
    idUsuario      = db.Column(db.Integer, primary_key=True)
    nombreUsuario  = db.Column(db.String(20), index=True, unique=True)
    nombreCompleto = db.Column(db.String(64))
    clave          = db.Column(db.String(255))
    correo         = db.Column(db.String(64), index=True, unique=True)

    def __init__(self, nombreUsuario, nombreCompleto, clave, correo):
        self.nombreUsuario  = nombreUsuario
        self.nombreCompleto = nombreCompleto
        self.clave          = clave
        self.correo         = correo

    def __repr__(self):
        return '<Usuario_%r %r>' % (self.idUsuario, self.nombreUsuario)



class clsDiseno(db.Model):
    '''Esquema de los disenos que realiza un usuario. 
       Un diseno esta compuesto por un conjunto de diagramas.'''

    __tablename__  = 'diseno'
    idDiseno    = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(64), index=True)
    descripcion = db.Column(db.Text())
    idCreador   = db.Column(db.Integer)
    propiedades = db.Column(db.Text())

    def __init__(self, nombre, descripcion, idCreador, propiedades):
        self.nombre      = nombre
        self.descripcion = descripcion
        self.idCreador   = idCreador
        self.propiedades = propiedades

    def __repr__(self):
        return '<Diseno_%r %r>' % (self.idDiseno, self.nombre)



class clsDisenosAsociadosUsuario(db.Model):
    '''Esquema de la tabla que almacena cuales disenos estan asociados
       a cuales usuarios.'''

    __tablename__ = 'disenosAsociadosUsuario'
    idAsociacion  = db.Column(db.Integer, primary_key=True)
    idDiseno      = db.Column(db.Integer, db.ForeignKey('diseno.idDiseno'))
    refDiseno     = db.relationship('clsDiseno', backref=db.backref('disenosAsociadosUsuario',
    	                                         lazy='dynamic'))
    idUsuario     = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
    refUsuario    = db.relationship('clsUsuario', backref=db.backref('disenosAsociadosUsuario',
    	                                          lazy='dynamic'))

    def __init__(self, idDiseno, idUsuario):
        self.idDiseno  = idDiseno
        self.idUsuario = idUsuario

    def __repr__(self):
        return '<Diseno %r asociado al usuario %r>' % (self.idDiseno, self.idUsuario)		



class clsDiagrama(db.Model):
    '''Esquema de los diagramas que describen casos de uso.'''

    __tablename__  = 'diagrama'
    idDiagrama  = db.Column(db.Integer, primary_key=True) 
    nombre      = db.Column(db.String(60))
    descripcion = db.Column(db.Text())
    propiedades = db.Column(db.Text())
    idDiseno    = db.Column(db.Integer, db.ForeignKey('diseno.idDiseno'))
    refDiseno   = db.relationship('clsDiseno', backref=db.backref('diagrama', 
                                               lazy='dynamic'))
        
    def __init__(self, nombre, descripcion, propiedades, idDiseno):
        self.nombre      = nombre
        self.descripcion = descripcion
        self.propiedades = propiedades
        self.idDiseno    = idDiseno

    def __repr__(self):
        return '<Diagrama_%r %r>' % (self.idDiagrama, self.nombre)



class clsEntidad(db.Model):
    '''Esquema de las entidades que tienen asociadas los disenos y las 
       operaciones de los diagramas.'''

    __tablename__ = 'entidad'
    idEntidad   = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(60))
    propiedades = db.Column(db.Text())
    idDiseno    = db.Column(db.Integer, db.ForeignKey('diseno.idDiseno'))
    refDiseno   = db.relationship('clsDiseno', backref=db.backref('entidad',
                                                  lazy='dynamic'))

    def __init__(self, nombre, propiedades, idDiseno):
        self.nombre      = nombre
        self.propiedades = propiedades
        self.idDiseno    = idDiseno

    def __repr__(self):
        return '<Entidad_%r %r>' % (self.idEntidad, self.nombre) 



class clsNodo(db.Model):
    '''Esquema de los nodos pertenecientes a un diagrama.'''

    __tablename__  = 'nodo'
    idNodo      = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(60))
    tipo        = db.Column(db.Integer)
    propiedades = db.Column(db.Text())
    idDiagrama  = db.Column(db.Integer, db.ForeignKey('diagrama.idDiagrama'))
    refDiagrama = db.relationship('clsDiagrama', foreign_keys=[idDiagrama],
                                                 backref=db.backref('nodo', 
                                                 lazy='dynamic'))
    __mapper_args__ = {
        'polymorphic_on':tipo,
        'polymorphic_identity':0
    }
        
    def __init__(self, nombre, tipo, propiedades, idDiagrama):
        self.nombre      = nombre
        self.tipo        = tipo
        self.propiedades = propiedades
        self.idDiagrama  = idDiagrama

    def __repr__(self):
        return '<' + self.tipo.capitalize() + '_%r %r>' % (self.idNodo, self.nombre)



class clsVista(clsNodo):
    '''Esquema del tipo de nodo Vista. Hereda el comportamiento de clsNodo.'''
    __mapper_args__ = {'polymorphic_identity': 1}

    def __repr__(self):
        return '<Vista_%r %r>' % (self.idNodo, self.nombre)    



class clsAccion(clsNodo):
    '''Esquema del tipo de nodo Accion. Hereda el comportamiento de clsNodo.'''
    __mapper_args__ = {'polymorphic_identity': 2}

    def __repr__(self):
        return '<Accion_%r %r>' % (self.idNodo, self.nombre)  



class clsOperacion(clsNodo):
    '''Esquema del tipo de nodo Operacion. Hereda el comportamiento de clsNodo.'''
    __mapper_args__ = {'polymorphic_identity': 3}

    idEntidad  = db.Column(db.Integer, db.ForeignKey('entidad.idEntidad'))
    refEntidad = db.relationship('clsEntidad', backref=db.backref('nodo',
                                               lazy='dynamic'))

    def __init__(self, nombre, tipo, propiedades, idDiagrama, idEntidad):
        self.nombre      = nombre
        self.tipo        = tipo
        self.propiedades = propiedades
        self.idDiagrama  = idDiagrama
        self.idEntidad   = idEntidad

    def __repr__(self):
        return '<Operacion_%r %r>' % (self.idNodo, self.nombre)   



class clsExterno(clsNodo):
    '''Esquema del tipo de nodo Accion. Hereda el comportamiento de clsNodo.'''
    __mapper_args__ = {'polymorphic_identity': 4}

    idNodoExterno  = db.Column(db.Integer, db.ForeignKey('nodo.idNodo'))
    refNodoExterno = db.relationship('clsNodo', foreign_keys=[idNodoExterno])

    def __init__(self, nombre, tipo, propiedades, idDiagrama, idNodoExterno):
        self.nombre        = nombre
        self.tipo          = tipo
        self.propiedades   = propiedades
        self.idDiagrama    = idDiagrama
        self.idNodoExterno = idNodoExterno

    def __repr__(self):
        return '<Externo_%r %r>' % (self.idNodo, self.nombre)



class clsRelacion(db.Model):
    '''Esquema de las relaciones pertenecientes a un diagrama.'''

    __tablename__  = 'relacion'
    idRelacion     = db.Column(db.Integer, primary_key=True)
    nombre         = db.Column(db.String(60), nullable=True)
    tipo           = db.Column(db.Integer)
    propiedades    = db.Column(db.Text())
    idNodoOrigen   = db.Column(db.Integer, db.ForeignKey('nodo.idNodo'))
    refNodoOrigen  = db.relationship('clsNodo', backref=db.backref('salientes', 
                                                lazy='dynamic'),
                                                foreign_keys=[idNodoOrigen])
    idNodoDestino  = db.Column(db.Integer, db.ForeignKey('nodo.idNodo'))
    refNodoDestino = db.relationship('clsNodo', backref=db.backref('entrantes', 
                                                lazy='dynamic'),
                                                foreign_keys=[idNodoDestino])
    idDiagrama     = db.Column(db.Integer, db.ForeignKey('diagrama.idDiagrama'))
    refDiagrama    = db.relationship('clsDiagrama', backref=db.backref('relacion', 
                                                    lazy='dynamic'))

    def __init__(self, nombre, tipo, propiedades, idNodoOrigen, idNodoDestino, idDiagrama):
        self.nombre        = nombre 
        self.tipo          = tipo
        self.propiedades   = propiedades
        self.idNodoOrigen  = idNodoOrigen
        self.idNodoDestino = idNodoDestino
        self.idDiagrama    = idDiagrama

    def __repr__(self):
        return '<Relacion_%r tipo %r Nodo_%r-Nodo_%r>' \
                    % (self.idRelacion, self.tipo, self.idNodoOrigen, self.idNodoDestino)


class clsEstiloNodo(db.Model):
    '''Esquema de los estilos pertenecientes a los nodos y la informacion de presentacion'''

    __tablename__ = 'estiloNodo'
    idEstiloNodo = db.Column(db.Integer, primary_key=True)
    idDiagrama   = db.Column(db.Integer, db.ForeignKey('diagrama.idDiagrama'))
    refDiagrama  = db.relationship('clsDiagrama', backref=db.backref('estiloNodo',
                                                  lazy='dynamic'))
    idNodo       = db.Column(db.Integer, db.ForeignKey('nodo.idNodo'))
    refNodo      = db.relationship('clsNodo', backref=db.backref('diagramas',
                                              lazy='dynamic'))
    propiedades  = db.Column(db.Text())

    def __init__(self, idDiagrama, idNodo, propiedades):
        self.idDiagrama  = idDiagrama
        self.idNodo      = idNodo
        self.propiedades = propiedades

    def __repr__(self):
        return '<EstiloNodo %r-%r>' % (self.idDiagrama, self.idNodo)


class clsEstiloRelacion(db.Model):
    '''Esquema de los estilos pertenecientes a las relaciones y la informacion de presentacion'''

    __tablename__ = 'estiloRelacion'
    idEstiloRelacion = db.Column(db.Integer, primary_key=True)
    idDiagrama       = db.Column(db.Integer, db.ForeignKey('diagrama.idDiagrama'))
    refDiagrama      = db.relationship('clsDiagrama', backref=db.backref('estiloRelacion',
                                                      lazy='dynamic'))
    idRelacion       = db.Column(db.Integer, db.ForeignKey('relacion.idRelacion'))
    refRelacion      = db.relationship('clsRelacion', backref=db.backref('diagramas',
                                                  lazy='dynamic'))
    propiedades      = db.Column(db.Text())

    def __init__(self, idDiagrama, idRelacion, propiedades):
        self.idDiagrama = idDiagrama
        self.idRelacion = idRelacion
        self.propiedades = propiedades

    def __repr__(self):
        return '<EstiloRelacion %r-%r>' % (self.idDiagrama, self.idRelacion)
        

db.create_all()


    #############################################
    #              Funciones Utiles             #
    #############################################

# def crearBaseDatos():
#     '''Permite crear la base de datos con la configuracion previa.'''
#     db.create_all()
        

# def resetBaseDatos():
#     '''Permite borrar la base de datos y crearla de nuevo.'''
#     db.drop_all()
#     db.create_all()


# def borrarBaseDatos():
#     '''Permite borrar la base de datos.'''
#     db.drop_all()

# Fin Clase BaseDatos
