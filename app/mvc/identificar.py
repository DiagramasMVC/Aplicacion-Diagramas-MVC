# -*- coding: utf-8 -*-
from flask import request, session, Blueprint, json

from app.model.claseUsuario       import *
from app.model.claseControlAcceso import *


ident = Blueprint('identificar', __name__)
login = ControlAcceso()
usr   = Usuario()


@ident.route('/identificar/AIdentificar', methods=['POST'])
def AIdentificar():
    # Parametros POST.
    params  = request.get_json()

    results = [{'label':'/VDisenos', 'msg':['Bienvenido a la aplicación'], }, 
               {'label':'/VLogin', 'msg':['Datos de identificación incorrectos']}, ]

    # Asignamos un mensaje a mostrar por defecto.
    res = results[0]

    # Mostramos el nombre de usuario en la aplicación.
    session['usuario'] = {'nombre': 'Aldrix', 'username': 'aldrix'}

    return json.dumps(res)


 
@ident.route('/identificar/ARegistrar', methods=['POST'])
def ARegistrar():
    params  = request.get_json()

    results = [{'label':'/VLogin', 'msg':['Felicitaciones, Ya estás registrado en la aplicación']}, 
               {'label':'/VRegistro', 'msg':['Error al tratar de registrarse']}, ]
    
    #  Mensaje a mostrar por defecto.
    res = results[0]

    nombreUsuario = params['nombre']
    nombre        = params['usuario']
    clave         = params['clave2']
    correo        = params['correo']

    return json.dumps(res)



@ident.route('/identificar/VLogin')
def VLogin():
    print("Estoy en VLogin")
    res = {}

    return json.dumps(res)



@ident.route('/identificar/VRegistro')
def VRegistro():
    print("Estoy en VRegistro")
    res = {}

    return json.dumps(res)