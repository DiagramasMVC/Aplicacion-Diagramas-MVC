# -*- coding: utf-8 -*-

from flask import request, session, Blueprint, json
from app.model.claseUsuario  import *
from app.model.claseDiseno   import *
from app.model.claseDiagrama import *
from app.model.claseEntidad  import *


dise = Blueprint('diseno', __name__)

usr  = Usuario()
dis  = Diseno()
diag = Diagrama()
ent  = Entidad()


@dise.route('/diseno/ACrearDiseno', methods=['POST'])
def ACrearDiseno():
    params  = request.get_json()
    results = [{'label':'/VDisenos', 'msg':['Diseño creado.']}, 
               {'label':'/VDisenos', 'msg':['El nombre de diseño ya existe.']},
               {'label':'/VDisenos', 'msg':['Error al crear diseño.']}, ]

    # Asignamos el mensaje a mostrar por defecto.
    res = results[2]

    # Extraemos los parametros
    nombreDiseno = params['nombre']
    descDiseno   = params['descripcion']

    # Obtenemos el usuario que esta creando el diseño.
    nombreUsuario = session['usuario']['username'] 
    
    result = usr.crearUsuario('aldrix', 'Aldrix Marfil', '1234', 'am@hotmail.com')
    
    # Obtenemos el id del usuario que creo el diseño.
    idUsuario = usr.obtenerUsuarioPorNombreUsuario(nombreUsuario).idUsuario

    if idUsuario:
        # Obtenemos los disenos asociados al usuario.
        listaDisenos = dis.obtenerDisenosPorUsuario(idUsuario)

        # Buscamos si alguno de esos disenos se llama igual al que se va a crear.
        existe = False
        for d in listaDisenos:
            if d.nombre.lower() == nombreDiseno.lower():
                existe = True
                break

        # Creamos el nuevo diseño.
        if existe:
            res = results[1]
        else:
            creado = dis.crearDiseno(nombreDiseno, descDiseno, idUsuario, json.dumps({}))

            if creado:
                res = results[0]

    return json.dumps(res)


 
@dise.route('/diseno/AModificarDiseno', methods=['POST'])
def AModificarDiseno():
	# Paramatros POST.
    params  = request.get_json()
    results = [{'label':'/VDisenos', 'msg':['Diseño actualizado.']}, 
    		   {'label':'/VDisenos', 'msg':['Error al actualizar diseño.']},]
    
    # Asignamos un mensaje a mostrar por defecto.
    res = results[1]

    # Obtenemos los parametros.
    nuevoNombre      = params['nombre']
    nuevaDescripcion = params['descripcion']
    idDiseno         = params['idDiseno']

    #  Buscamos el diseno a modificar.
    diseno = dis.obtenerDisenoPorID(idDiseno)

    modificado = dis.actualizarDiseno(idDiseno, nuevoNombre, nuevaDescripcion, diseno.propiedades)

    if modificado:
        res = results[0]

    return json.dumps(res)



@dise.route('/diseno/AEliminarDiseno', methods=['GET'])
def AEliminarDiseno():
    console.log("llego a eliminar");
	# Paramatros POST.
    params  = request.get_json()
    results = [{'label':'/VDiseno', 'msg':['Diseño eliminado.']}, ]
    res     = results[0]
    return json.dumps(res)



@dise.route('/diseno/VDiseno')
def VDiseno():
    print(session)
    res = {}

    # Obtenemos el id del diseño.
    idDiseno = int(request.args.get('idDiseno',1))

    if 'usuario' not in session:
      res['logout'] = '/'
      return json.dumps(res)
    
    # Comunicamos a la vista el nombre de usuario actual.
    res['usuario'] = session['usuario']

    # Obtenemos los diagramas asociados al diseño actual.
    listaDiagramas = diag.obtenerDiagramasPorDiseno(idDiseno)

    res['data1'] = [{'idDiagrama': d.idDiagrama,
                     'nombre': d.nombre,
                     'descripcion': d.descripcion} for d in listaDiagramas]

    # Obtenemos las entidades asociadas al diseño actual.
    listaEntidades = ent.obtenerEntidadesPorDiseno(idDiseno)

    res['data2'] = [{'idEntidad': e.idEntidad,
                     'nombre': e.nombre} for e in listaEntidades]

    # Guardamos el id del diseño.
    session['idDiseno'] = idDiseno
    res['idDiseno'] = idDiseno

    return json.dumps(res)



@dise.route('/diseno/VDisenos')
def VDisenos():
    res = {}

    if 'usuario' not in session:
        res['logout'] = '/'
        return json.dumps(res)

    res['usuario'] = session['usuario']

    # Obtenemos el nombre del usuario.
    nombreUsuario = session['usuario']['username']

    # Obtenemos el id del usuario actual.
    usuario   = usr.obtenerUsuarioPorNombreUsuario(nombreUsuario)
    idUsuario = usuario.idUsuario

    # Obtenemos la lista de diseños a mostrar para este usuario.
    listaDisenos = dis.obtenerDisenosPorUsuario(idUsuario)

    res['data0'] = [{'idDiseno': d.idDiseno, 
                     'nombre': d.nombre, 
                     'descripcion': d.descripcion} for d in listaDisenos]

    return json.dumps(res)