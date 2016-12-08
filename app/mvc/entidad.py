# -*- coding: utf-8 -*-

from flask import request, session, Blueprint, json
from app.model.claseEntidad import *


ent = Blueprint('entidad', __name__)

enti = Entidad()


@ent.route('/entidad/ACrearEntidad', methods=['POST'])
def ACrearEntidad():
    params  = request.get_json()
    results = [{'label':'/VDiseno', 'msg':['Entidad creada']},
               {'label':'/VCrearEntidad', 'msg':['El nombre de la entidad ya existe']},
               {'label':'/VCrearEntidad', 'msg':['Error al crear entidad']},]

    # Asignamos el mensaje a mostrar por defecto.
    res = results[2]

    # Extraemos los parametros
    nombreEntidad = params['nombre']

    # Obtenemos el id del diseno al cual pertenece la entidad.
    idDiseno = int(request.args.get('idDiseno',1))

    # Obtenemos las entidades asociadas al diseno.
    listaEntidades = enti.obtenerEntidadesPorDiseno(idDiseno)

    # Buscamos si alguno de esas entidades se llama igual al que se va a crear.
    existe = False
    for e in listaEntidades:
        if e.nombre.lower() == nombreEntidad.lower():
            existe = True
            break

    # Creamos la nuevo entidad.
    if existe:
        res = results[1]
    else:
        creado = enti.crearEntidad(nombreEntidad, json.dumps({}), idDiseno)
        if creado:
            res = results[0]

    res['label'] = res['label'] + '/' + str(idDiseno)

    return json.dumps(res)



@ent.route('/entidad/AModificarEntidad', methods=['POST'])
def AModificarEntidad():
    params  = request.get_json()
    results = [{'label':'/VDiseno', 'msg':['Diagrama creado']},
               {'label':'/VEntidad', 'msg':['El nombre del diseño ya existe']},
               {'label':'/VEntidad', 'msg':['Error al actualizar el diseño']},]

    # Asignamos el mensaje a mostrar por defecto.
    res = results[0]

    return json.dumps(res)



@ent.route('/entidad/AEliminarEntidad', methods=['GET'])
def AEliminarEntidad():
    params  = request.get_json()
    results = [{'label':'/VDiseno', 'msg':['Diagrama creado']},
               {'label':'/VCrearDiagrama', 'msg':['El nombre del diagrama ya existe']},
               {'label':'/VCrearDiagrama', 'msg':['Error al crear diagrama']},]

    # Asignamos el mensaje a mostrar por defecto.
    res = results[0]

    return json.dumps(res)