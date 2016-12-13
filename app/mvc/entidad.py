# -*- coding: utf-8 -*-

from flask import request, session, Blueprint, json
from app.model.claseEntidad  import *
from app.model.claseDiagrama import *
from app.model.claseNodo     import *
from app.model.claseRelacion import *
from app.model.claseEstiloNodo     import *
from app.model.claseEstiloRelacion import *


ent = Blueprint('entidad', __name__)

enti  = Entidad()
diag  = Diagrama()
nodo  = Nodo()
eNodo = EstiloNodo()
rela  = Relacion()
eRela = EstiloRelacion()


@ent.route('/entidad/ACrearEntidad', methods=['POST'])
def ACrearEntidad():
    params  = request.get_json()
    results = [{'label':'/VDiseno', 'msg':['Entidad creada']},
               {'label':'/VDiseno', 'msg':['El nombre de la entidad ya existe']},
               {'label':'/VDiseno', 'msg':['Error al crear entidad']},]

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
    results = [{'label':'/VDiseno', 'msg':['Entidad modificada']},
               {'label':'/VDiseno', 'msg':['El nombre de la entidad ya existe']},
               {'label':'/VDiseno', 'msg':['Error al actualizar la entidad']},]

    # Asignamos el mensaje a mostrar por defecto.
    res = results[2]

    # Extraemos los parametros.
    nuevoNombre = params['nombre']
    idEntidad   = params['idEntidad']

    #Obtenemos el id del diseno al cual pertenece la entidad.
    idDiseno = int(request.args.get('idDiseno',1))

    #  Obtenemos las entidades asociadas a l diseno.
    listaEntidades = enti.obtenerEntidadesPorDiseno(idDiseno)

    # Buscamos si alguna de esas entidades se llama igual al que se va a crear.
    existe = False
    for e in listaEntidades:
        if e.nombre.lower() == nuevoNombre.lower():
            existe = True
            break

    if existe:
        res = results[1]
    else:
        # Buscamos la entidad a modificar.
        diagrama = enti.obtenerEntidadPorID(idEntidad)

        modificado = enti.actualizarEntidad(idEntidad, nuevoNombre, idDiseno)

        if modificado:
            res = results[0]

    res['label'] = res['label'] + '/' + str(idDiseno)    

    return json.dumps(res)



@ent.route('/entidad/AEliminarEntidad', methods=['GET'])
def AEliminarEntidad():
    params  = request.get_json()
    results = [{'label':'/VDiseno', 'msg':['Entidad eliminada']},
               {'label':'/VDiseno', 'msg':['Error al eliminar la entidad']},]

    # Asignamos el mensaje a mostrar por defecto.
    res = results[1]

    # Obtenemos el id de la entidad que queremos eliminar.
    idEntidad = int(request.args.get('idEntidad',1))

    # Obtenemos la entidad a eliminar.
    entidad = enti.obtenerEntidadPorID(idEntidad)
    print("Entidad a eliminar", entidad.nombre)

    # Obtenemos el id del diseno al cual pertenece la entidad.
    idDiseno = int(request.args.get('idDiseno',1))

    # Antes de eliminar la entidad debemos buscar cuales son las operaciones que la usan.
    listaDiagramas = diag.obtenerDiagramasPorDiseno(idDiseno)
    print("Buscamos las operaciones en los diagramas")

    for d in listaDiagramas:
        operaciones = nodo.obtenerNodosOperacionPorDiagramaYEntidad(d.idDiagrama, idEntidad)

        # Eliminamos las relaciones entre las operaciones y las acciones.
        for o in operaciones:
            print("Encontramos la operacion asociada a la entidad", o.nombre, o.idDiagrama)
            relacion = rela.obtenerRelacionNoDirigidaOperacionAccion(o.idNodo)

            if relacion != None:
                elim1 = rela.eliminarRelacionPorID(relacion.idRelacion)
                elim2 = eRela.eliminarEstiloNodoAsociadoAUnaRelacion(relacion.idRelacion)
                print("se elimino la relacion y su estilo nodo", elim1, elim2)

            eliminado = nodo.eliminarNodoPorId(o.idNodo)
            print("se elimino el nodo", eliminado)
            eliminado = eNodo.eliminarEstiloNodoAsociadoAUnNodo(o.idNodo)

    eliminado1 = enti.eliminarEntidadPorID(idEntidad)
    eliminado2 = eNodo.eliminarEstiloNodoAsociadoAUnNodo(idEntidad)

    if eliminado1 and eliminado2:
        res = results[0]

    res['label'] = res['label'] + '/' + str(idDiseno)   

    return json.dumps(res)