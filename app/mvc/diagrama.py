# -*- coding: utf-8 -*-

from flask import request, session, Blueprint, json
from app.model.claseDiseno     import *
from app.model.claseDiagrama   import *
from app.model.claseNodo       import *
from app.model.claseRelacion   import *
from app.model.claseEstiloNodo import *
from app.model.claseEntidad    import *


diag = Blueprint('diagrama', __name__)

TIPO_VISTA     = 1
TIPO_ACCION    = 2
TIPO_OPERACION = 3
TIPO_EXTERNO   = 4

TIPO_VISTA_ACCION   = 1
TIPO_ACCION_OPERACION  = 2
TIPO_VISTA_EXTERNO  = 3
TIPO_ACCION_EXTERNO = 4

dis = Diseno()
dia = Diagrama()
nodo = Nodo()
rela = Relacion()
eNodo = EstiloNodo()
ent = Entidad()


@diag.route('/diagrama/ACrearDiagrama', methods=['POST'])
def ACrearDiagrama():
    params  = request.get_json()
    results = [{'label':'/VDiseno', 'msg':['Diagrama creado']},
               {'label':'/VDiseno', 'msg':['El nombre del diagrama ya existe']},
               {'label':'/VDiseno', 'msg':['Error al crear diagrama']},]

    # Asignamos el mensaje a mostrar por defecto.
    res = results[2]

    # Extraemos los parametros
    nombreDiagrama = params['nombre']
    descDiagrama   = params['descripcion']

    # Obtenemos el id del diseno al cual pertenece el diagrama.
    idDiseno = int(request.args.get('idDiseno',1))

    # Obtenemos los diagramas asociados al diseno.
    listaDiagramas = dia.obtenerDiagramasPorDiseno(idDiseno)

    # Buscamos si alguno de esos diagramas se llama igual al que se va a crear.
    existe = False
    for d in listaDiagramas:
        if d.nombre.lower() == nombreDiagrama.lower():
            existe = True
            break

        # Creamos el nuevo diagrama.
    if existe:
        res = results[1]
    else:
        creado = dia.crearDiagrama(nombreDiagrama, descDiagrama, json.dumps({}), idDiseno)
        if creado:
            res = results[0]

    res['label'] = res['label'] + '/' + str(idDiseno)

    return json.dumps(res)



@diag.route('/diagrama/AModificarDiagrama', methods=['POST'])
def AModificarDiagrama():
    params  = request.get_json()
    results = [{'label':'/VDiseno', 'msg':['Diagrama creado']},
               {'label':'/VCrearDiagrama', 'msg':['El nombre del diagrama ya existe']},
               {'label':'/VCrearDiagrama', 'msg':['Error al crear diagrama']},]

    # Asignamos el mensaje a mostrar por defecto.
    res = results[2]

    # Extraemos los parametros
    nombreDiagrama = params['nombre'] 
    descDiagrama   = params['descripcion']

    #Obtenemos el id del diseno al cual pertenece el diagrama.
    idDiseno = int(session['idDiseno'])

    return json.dumps(res)



@diag.route('/diagrama/AEliminarDiagrama', methods=['GET'])
def AEliminarDiagrama():
    params  = request.get_json()
    results = [{'label':'/VDiseno', 'msg':['Diagrama creado']},
               {'label':'/VCrearDiagrama', 'msg':['El nombre del diagrama ya existe']},
               {'label':'/VCrearDiagrama', 'msg':['Error al crear diagrama']},]

    # Asignamos el mensaje a mostrar por defecto.
    res = results[2]

    # Extraemos los parametros
    nombreDiagrama = params['nombre'] 
    descDiagrama   = params['descripcion']

    #Obtenemos el id del diseno al cual pertenece el diagrama.
    idDiseno = int(session['idDiseno'])

    return json.dumps(res)



@diag.route('/diagrama/VDiagrama')
def VDiagrama():
    res = {}

    # Obtenemos el id del diagrama.
    idDiagrama = int(request.args.get('idDiagrama',1))
    idDiseno   = int(request.args.get('idDiseno',1))
    

    if 'usuario' not in session:
      res['logout'] = '/'
      return json.dumps(res)

    # Comunicamos a la vista el nombre de usuario actual.
    res['usuario'] = session['usuario']

    # Obtenemos los datos del diagrama actual.
    diagrama = dia.obtenerDiagramaPorID(idDiagrama)

    # Obtenemos los datos asociados al diagrama.
    res['fDiagrama'] = {'idDiagrama': idDiagrama, 
                        'nombre': diagrama.nombre, 
                        'descripcion': diagrama.descripcion}


    # Obtenemos los datos asociados al diseno actual.
    listaDiagramas = dia.obtenerDiagramasPorDiseno(idDiseno)

    # Obtenemos los datos asociados al diseño.
    res['fDiagrama_opcionesDiagrama'] = [{'key':d.idDiagrama, 
                                          'value':d.nombre} for d in listaDiagramas]


    res['fElemento_opcionesTipo'] = [{'key':TIPO_VISTA, 'value':'Vista'},
                                     {'key':TIPO_ACCION, 'value':'Acción'},
                                     {'key':TIPO_OPERACION, 'value':'Operación'}]

    # Obtenemos las entidades asociadas al diseño.
    listaEntidades = ent.obtenerEntidadesPorDiseno(idDiseno)

    res['fElemento_opcionesEntidad'] = [{'key': e.idEntidad, 'value': e.nombre} for e in listaEntidades]

    # Obtenemos los datos de los elementos asociados al diagrama actual.

    nodo = Nodo()
    # Vistas
    listaVistas     = nodo.obtenerNodosVistaPorDiagrama(idDiagrama)
    vistasPorDiseno = nodo.obtenerNodosVistaPorDiseno(idDiseno)

    # Obtenemos los id de las vistas del diagrama actual.
    idVistas = []
    for v in listaVistas:
        idVistas.append(v.idNodo)

    # Vistas que pertenecen al diagrama.
    res['fAccion_opcionesVistaInterna'] = [{'key': v.idNodo, 'value': v.nombre} for v in listaVistas]
    res['fAccion_opcionesVistaInterna'].append({'key': 0, 'value': 'Ninguna'})

    # Quitamos las vistas que pertenecen al diagrama actual.
    listaVistasExternas = []
    for v in vistasPorDiseno:
        if not v.idNodo in idVistas:
            listaVistasExternas.append(v)

    # Vistas de otros diagramas.
    res['fAccion_opcionesVistaExterna'] = [{'key': v.idNodo, 'value': v.nombre} for v in listaVistasExternas]
    res['fAccion_opcionesVistaExterna'].append({'key': 0, 'value': 'Ninguna'})

    vistas = []
    for v in listaVistas:
        estiloNodo = eNodo.obtenerEstiloNodoPorIdNodo(v.idNodo)
        vistas.append({'id': v.idNodo, 'nombre': v.nombre, 'x': json.loads(estiloNodo.propiedades)['x'], 'y': json.loads(estiloNodo.propiedades)['y'], 'atributos': json.loads(v.propiedades)['atributos']})
        
    # Acciones 
    listaAcciones = nodo.obtenerNodosAccionPorDiagrama(idDiagrama)
    accionesPorDiseno = nodo.obtenerNodosAccionPorDiseno(idDiseno)

    # Obtenemos los id de las acciones del diagrama actual.
    idAcciones = []
    for a in listaAcciones:
        idAcciones.append(a.idNodo)

    acciones = []
    for a in listaAcciones:
        relaInternas = rela.obtenerRelacionesDirigidasAccionVista(a.idNodo)
        relaExternas = rela.obtenerRelacionesDirigidasAccionExterno(a.idNodo)
        
        lista_relaInternas = []
        lista_relaExternas = []
        for r in relaInternas:
            n = nodo.obtenerNodoPorID(r.idNodoDestino)
            lista_relaInternas.append({'idVista': r.idNodoDestino, 'nombre': n.nombre})

        for r in relaExternas:
            n = nodo.obtenerNodoPorID(r.idNodoDestino)
            lista_relaExternas.append({'idVista': r.idNodoDestino, 'nombre': n.nombre, 'nodo_real': n.idNodoExterno})

        estiloNodo = eNodo.obtenerEstiloNodoPorIdNodo(a.idNodo)
        acciones.append({'id': a.idNodo, 'nombre': a.nombre, 'x': json.loads(estiloNodo.propiedades)['x'], 'y': json.loads(estiloNodo.propiedades)['y'], "vista_interna": 0, "vista_externa": 0, "relaciones_internas": lista_relaInternas, "relaciones_externas": lista_relaExternas})

    # Acciones que pertenecen al diagrama.
    res['fVista_opcionesAccionInterna'] = [{'key': a.idNodo, 'value': a.nombre} for a in listaAcciones]
    res['fVista_opcionesAccionInterna'].append({'key': 0, 'value': 'Ninguna'})

    # Quitamos las acciones que pertenecen al diagrama actual.
    listaAccionesExternas = []
    
    for a in accionesPorDiseno:
        if not a.idNodo in idAcciones:
            listaAccionesExternas.append(a)

    # Acciones que externas al diagrama.
    res['fVista_opcionesAccionExterna'] = [{'key': a.idNodo, 'value': a.nombre} for a in listaAccionesExternas]
    res['fVista_opcionesAccionExterna'].append({'key': 0, 'value': 'Ninguna'})

    # Relaciones Operacion-Accion
    listaAccOp = rela.obtenerRelacionesPorTipoYDiagrama(TIPO_ACCION_OPERACION, idDiagrama)

    accOp = []
    for r in listaAccOp:
        accOp.append({'origen': r.idNodoOrigen, 'destino': r.idNodoDestino})

    # Operaciones
    listaOperaciones = nodo.obtenerNodosOperacionPorDiagrama(idDiagrama)
    
    operaciones = []
    idAccion = 0
    for o in listaOperaciones:
        estiloNodo = eNodo.obtenerEstiloNodoPorIdNodo(o.idNodo)

        # Obtenmos la accion con la cual esta asociado.
        for r in accOp:
            if o.idNodo == r['origen']:
                idAccion = r['destino']
        operaciones.append({'id': o.idNodo, 'nombre': o.nombre, 'x': json.loads(estiloNodo.propiedades)['x'], 'y': json.loads(estiloNodo.propiedades)['y'], 'idEntidad': o.idEntidad, 'idAccion': idAccion})

    # Nodos Externos.
    listaExternos = nodo.obtenerNodosExternoPorDiagrama(idDiagrama)

    externos = []
    for e in listaExternos:
        estiloNodo = eNodo.obtenerEstiloNodoPorIdNodo(e.idNodo)

        # Obtenemos el nodo externo con el cual esta asociado.
        externos.append({'id': e.idNodo, 'nombre': e.nombre, 'x': json.loads(estiloNodo.propiedades)['x'], 'y': json.loads(estiloNodo.propiedades)['y']})

    # Obtenemos las relaciones dirigidas vista-accion.
    relaciones = rela.obtenerRelacionesPorTipoYDiagrama(TIPO_VISTA_ACCION, idDiagrama)

    accVis = []
    visAcc = []
    for r in relaciones:
        oNodo = nodo.obtenerNodoPorID(r.idNodoOrigen)
        if oNodo.tipo == TIPO_ACCION:
            accVis.append({'origen': r.idNodoOrigen, 'destino': r.idNodoDestino})
        else:
            id_salida = json.loads(r.propiedades)['id_salida']
            visAcc.append({'origen': r.idNodoOrigen, 'destino': r.idNodoDestino, 'id_salida': id_salida})

    # Obtenemos las relaciones dirigidas accion-externo y externo-accion.
    relaciones = rela.obtenerRelacionesPorTipoYDiagrama(TIPO_ACCION_EXTERNO, idDiagrama)

    accExt = []
    extAcc = []
    for r in relaciones:
        oNodo = nodo.obtenerNodoPorID(r.idNodoOrigen)
        if oNodo.tipo == TIPO_ACCION:
            accExt.append({'origen': r.idNodoOrigen, 'destino': r.idNodoDestino})
        else:
            extAcc.append({'origen': r.idNodoOrigen, 'destino': r.idNodoDestino})

    # Obtenemos las relaciones dirigidas externo-vista y vista-externo.
    relaciones = rela.obtenerRelacionesPorTipoYDiagrama(TIPO_VISTA_EXTERNO, idDiagrama)

    visExt = []
    extVis = []
    for r in relaciones:
        oNodo = nodo.obtenerNodoPorID(r.idNodoOrigen)
        if oNodo.tipo == TIPO_VISTA:
            id_salida = json.loads(r.propiedades)['id_salida']
            visExt.append({'origen': r.idNodoOrigen, 'destino': r.idNodoDestino, 'id_salida': id_salida})
        else:
            extVis.append({'origen': r.idNodoOrigen, 'destino': r.idNodoDestino})

    print('\n\nNODOS')
    print('Nodos vista', vistas, '\n')
    print('Nodos accion', acciones, '\n')
    print('Nodos operacion:', operaciones, '\n')
    print('Nodos externo:', externos, '\n')
    print('\nENLACES')
    print('Enlaces vista-accion', visAcc, '\n')
    print('Enlaces accion-vista', accVis, '\n')
    print('Enlaces vista-externo:', visExt, '\n')
    print('Enlaces externo-vista:', extVis, '\n')
    print('Enlaces accion-externo:', accExt, '\n')
    print('Enlaces externo-accion:', extAcc, '\n')
    print('Enlaces accion-operacion:', accOp, '\n')   


    res['data5'] = {"nodos":
                     [{"vistas"     : vistas}, 
                      {"acciones"   : acciones},
                      {"operaciones": operaciones},
                      {"externos"   : externos}
                     ], 
                    "enlaces":
                      [{"visAcc": visAcc},
                      {"accVis" : accVis},
                      {"visExt" : visExt},
                      {"extVis" : extVis},
                      {"accExt" : accExt},
                      {"extAcc" : extAcc},
                      {"accOp"  : accOp}
                      ]
                  };

    # res['data5'] = {"nodos":
    #                   [{"vistas":
    #                      [{"id":1, "nombre":"VRegistrar", "x":120,"y":80,
    #                         "elementos":
    #                           [{"id":1,"nombre":"Entrada1"},
    #                            {"id":2,"nombre":"Salida1"},
    #                            {"id":3,"nombre":"Entrada2"},
    #                            {"id":4,"nombre":"Salida2"}]
    #                       },
    #                       {"id":2, "nombre":"VIniciar", "x":120,"y":520,
    #                         "elementos":
    #                           [{"id":1,"nombre":"Entrada1"},
    #                            {"id":2,"nombre":"Salida1"},
    #                            {"id":3,"nombre":"Entrada2"}]
    #                       }, 
    #                       {"id":3, "nombre":"VLogin", "x":380,"y":80,
    #                       "elementos":
    #                           [{"id":1,"nombre":"Entrada1"},
    #                            {"id":2,"nombre":"SalidaSuperHiperLarga"},
    #                            {"id":3,"nombre":"Entrada2"},
    #                            {"id":4,"nombre":"Salida2"}]
    #                       }, 
    #                       {"id":4, "nombre":"VEjemplo", "x":380,"y":290,
    #                         "elementos":
    #                           [{"id":1,"nombre":"Entrada1"},
    #                            {"id":2,"nombre":"Salida1"},
    #                            {"id":3,"nombre":"Entrada2"},
    #                            {"id":4,"nombre":"Salida2"}]
    #                       },  
    #                       {"id":5, "nombre":"VCrear", "x":600,"y":520,
    #                         "elementos":
    #                           [{"id":1,"nombre":"Entrada1"},
    #                            {"id":2,"nombre":"Salida1"},
    #                            {"id":3,"nombre":"Entrada2"},
    #                            {"id":4,"nombre":"Salida2"}]
    #                       },
    #                       {"id":6, "nombre":"VEspecial", "x":600,"y":80,
    #                         "elementos":
    #                           []
    #                       }
    #                      ]}, 
    #                   {"acciones":
    #                     [{"id":21, "nombre":"ARegistrar", "x":120,"y":300},
    #                      {"id":22, "nombre":"ALogin", "x":380,"y":650},  
    #                      {"id":23, "nombre":"ACrear", "x":600,"y":300}
    #                     ]},
    #                   {"operaciones":
    #                     [{"id":31, "nombre":"Operacion1", "x":250,"y":390},
    #                      {"id":32, "nombre":"Operacion2", "x":85,"y":390},
    #                      {"id":33, "nombre":"Operacion3", "x":280,"y":750},
    #                      {"id":34, "nombre":"Operacion4", "x":460,"y":750}
    #                     ]},
    #                   {"externos":
    #                     [{"id":41, "nombre":"Externo1", "x":380,"y":430},
    #                      {"id":42, "nombre":"Externo2", "x":800,"y":80}
    #                     ]}
    #                  ], 
    #                 "enlaces":
    #                   [{"visAcc":
    #                     [{"origen":1,"destino":21,"puerto":1},
    #                      {"origen":1,"destino":21,"puerto":3},
    #                      {"origen":1,"destino":21,"puerto":2},
    #                      {"origen":1,"destino":21,"puerto":4},
    #                      {"origen":2,"destino":22,"puerto":1},
    #                      {"origen":2,"destino":22,"puerto":3},
    #                      {"origen":2,"destino":22,"puerto":2},
    #                      {"origen":5,"destino":23,"puerto":4},
    #                      {"origen":5,"destino":23,"puerto":3},
    #                      {"origen":5,"destino":23,"puerto":1},
    #                      {"origen":5,"destino":22,"puerto":4},
    #                      {"origen":5,"destino":22,"puerto":2}
    #                     ]},
    #                   {"accVis":
    #                     [{"origen":22,"destino":5,"puerto":225},
    #                      {"origen":21,"destino":2,"puerto":212}
    #                     ]},
    #                   {"accExt":
    #                     [{"origen":22,"destino":41}
    #                     ]},
    #                   {"extAcc":
    #                     [{"origen":42,"destino":23}
    #                     ]},
    #                   {"accOp":
    #                     [{"origen":21,"destino":31},
    #                      {"origen":21,"destino":32},
    #                      {"origen":22,"destino":33},
    #                      {"origen":22,"destino":34}
    #                     ]}
    #                   ]
    #               };



    res['fOperacion_opcionesAccion']  = [{'key': a.idNodo, 'value': a.nombre} for a in listaAcciones]
    res['fOperacion_opcionesAccion'].append({'key': 0, 'value': 'Ninguna'})

    res['fOperacion_opcionesEntidad'] = [{'key': e.idEntidad, 'value': e.nombre} for e in listaEntidades]

    # Guardamos el id del diseño.
    session['idDiagrama'] = idDiagrama
    session['idDiseno']   = idDiseno
    res['idDiagrama']     = idDiagrama
    res['idDiseno']       = idDiseno

    return json.dumps(res)



@diag.route('/diagrama/AGuardarPosicionDiagrama', methods=['POST'])
def AGuardarPosicionDiagrama():
    params  = request.get_json()

    # Buscamos el estilo nodo asociado al elemento.
    estiloNodo = eNodo.obtenerEstiloNodoPorIdNodo(params['id'])

    propiedades = json.loads(estiloNodo.propiedades)
    propiedades['x'] = params['x']
    propiedades['y'] = params['y']

    
    # Modificamos la posicion.
    eNodo.actualizarPropiedadesEstiloNodo(params['id'], json.dumps(propiedades))

    return json.dumps({})