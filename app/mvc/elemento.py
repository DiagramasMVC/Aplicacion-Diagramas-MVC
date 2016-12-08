# -*- coding: utf-8 -*-

from flask import request, session, Blueprint, json
from app.model.claseDiseno     import *
from app.model.claseDiagrama   import *
from app.model.claseNodo       import *
from app.model.claseRelacion   import *
from app.model.claseEstiloNodo import *
from app.model.claseEntidad    import *


elem = Blueprint('elemento', __name__)

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


@elem.route('/elemento/ACrearElemento', methods=['POST'])
def ACrearElemento():
    params  = request.get_json()
    results = [{'label':'/VDiagrama', 'msg':['Vista creada']},
               {'label':'/VDiagrama', 'msg':['Acción creada']},
               {'label':'/VDiagrama', 'msg':['Operación creada']},
               {'label':'/VDiagrama', 'msg':['El nombre de la vista ya existe']},
               {'label':'/VDiagrama', 'msg':['El nombre de la acción ya existe']},
               {'label':'/VDiagrama', 'msg':['El nombre de la operación ya existe']},
               {'label':'/VDiagrama', 'msg':['Error al crear elemento']},]

    # Asignamos el mensaje a mostrar por defecto.
    res = results[6]

    # Extraemos los parametros comunes.
    nombreElemento = params['nombre']
    tipoElemento   = params['tipo']

    # Obtenemos el id del diagrama al cual pertenece el elemento.
    idDiagrama = int(session['idDiagrama'])

    if tipoElemento == TIPO_VISTA:
        nombresAtributos = params['atributos']

        listaVistas = nodo.obtenerNodosVistaPorDiagrama(idDiagrama)

        # Buscamos si alguno de las vistas se llama igual que la que se va a crear.
        existe = False
        for v in listaVistas:
            if v.nombre.lower() == nombreElemento.lower():
                existe = True
                break

        # Creamos la nueva vista.
        if existe:
            res = results[3]
        else:
            creado = nodo.crearNodoVista(nombreElemento, json.dumps({'atributos':nombresAtributos}), idDiagrama)

            if creado:
                # Obtenemos el nodo creado.
                vista = None
                listaVistas = nodo.obtenerNodosVistaPorDiagrama(idDiagrama)

                for v in listaVistas:
                    if v.nombre == nombreElemento:
                        vista = v

                posIni = 80 + len(listaVistas)*(len(nombresAtributos)+1)*20

                creado = False
                if vista != None:
                    # Establecemos la posicion del nodo.
                    creado = eNodo.crearEstiloNodo(idDiagrama, vista.idNodo, json.dumps({"x": 200, "y": posIni}))

                if creado:
                    res = results[0]
                else: 
                    res = results[6]
                    nodo.eliminarNodoPorId(idNodo)


    elif tipoElemento == TIPO_ACCION:

        listaAcciones = nodo.obtenerNodosAccionPorDiagrama(idDiagrama)

        # Buscamos si alguno de las acciones se llama igual que la que se va a crear.
        existe = False
        for a in listaAcciones:
            if a.nombre.lower() == nombreElemento.lower():
                existe = True
                break

        # Creamos la nueva accion.
        if existe:
            res = results[4]
        else:
            creado = nodo.crearNodoAccion(nombreElemento, json.dumps({}), idDiagrama)
            
            if creado:
                # Obtenemos el nodo creado.
                accion = None
                listaAcciones = nodo.obtenerNodosAccionPorDiagrama(idDiagrama)

                for a in listaAcciones:
                    if a.nombre == nombreElemento:
                        accion = a

                posIni = 80 + len(listaAcciones)*80

                creado = False
                if accion != None:
                    # Establecemos la posicion del nodo.
                    creado = eNodo.crearEstiloNodo(idDiagrama, accion.idNodo, json.dumps({"x": 450, "y": posIni}))
                
                if creado:
                    res = results[1]
                else:
                    res = results[6]
                    nodo.eliminarNodoPorId(idNodo)


    elif tipoElemento == TIPO_OPERACION:
        idEntidad = params['idEntidad'] 

        listaOperaciones = nodo.obtenerNodosOperacionPorDiagrama(idDiagrama)

        # Buscamos si alguno de las operaciones se llama igual que la que se va a crear.
        existe = False
        for o in listaOperaciones:
            if o.nombre.lower() == nombreElemento.lower():
                existe = True
                break

        # Creamos la nueva operacion.
        if existe:
            res = results[5]
        else:
            creado = nodo.crearNodoOperacion(nombreElemento, json.dumps({}), idDiagrama, idEntidad)
            
            if creado:
                # Obtenemos el nodo creado.
                operacion = None
                listaOperaciones = nodo.obtenerNodosOperacionPorDiagrama(idDiagrama)

                for o in listaOperaciones:
                    if o.nombre == nombreElemento:
                        operacion = o

                posIni = 80 + len(listaOperaciones)*80

                creado = False
                if operacion != None:
                    # Establecemos la posicion del nodo.
                    creado = eNodo.crearEstiloNodo(idDiagrama, operacion.idNodo, json.dumps({"x": 750, "y": posIni}))
                
                if creado:
                    res = results[2]
                else:
                    res = results[6]
                    nodo.eliminarNodoPorId(operacion.idNodo)
                    # Eliminar estilo nodo tambien ###################################################################################################

    res['label'] = res['label'] + '/' + str(idDiagrama)

    return json.dumps(res)



@elem.route('/elemento/AModificarVista', methods=['POST'])
def AModificarVista():
    params  = request.get_json()
    results = [{'label':'/VDiagrama', 'msg':['Vista Modificada']},
               {'label':'/VDiagrama', 'msg':['Error al modificar vista']},]

    print('Parametros de AModificarVista', params)

    # Asignamos el mensaje a mostrar por defecto.
    res = results[1]

    # Obtenemos el id del diagrama y el diseño al cual pertenece el elemento.
    idDiagrama = int(session['idDiagrama'])
    idDiseno   = int(request.args.get('idDiseno',1))

    # Extraemos los parametros.
    idVista     = params['idNodo']
    nombreVista = params['nombre'] 
    atributos   = params['atributos']

    anterior = nodo.obtenerNodoPorID(idVista)

    # Agregamos los nuevos atributos.

    propiedades = json.loads(anterior.propiedades)
    propiedades['atributos'] = atributos

    actualizado = nodo.actualizarNodoVista(idVista, nombreVista, json.dumps(propiedades))
    
    # Actualizamos los nodos externos asociados a la vista actual.
    listaDiagramas = dia.obtenerDiagramasPorDiseno(idDiseno)

    for d in listaDiagramas:
        nd = nodo.obtenerNodoExternoAsociadoAlDiagrama(d.idDiagrama, idVista)

        # Si existe actualizamos el nodo externo.
        if nd != None:
            propiedades = json.loads(nd.propiedades)
            resultado = nodo.actualizarNodoExterno(nd.idNodo, nombreVista, json.dumps(propiedades), nd.idDiagrama, idVista)
            # idNodo, nuevoNombre, nuevasPropiedades, nuevoIdDiagrama, nuevoIdNodoExt

    creado1 = True
    creado2 = True
    creado3 = True
    # Creamos las nuevas relaciones vista-accion si las hay.
    for atr in atributos:
        if atr['accion_interna'] != 0:
            propiedades_rela = {"id_salida": atr['id']}
            # Buscamos si la relacion no existe.
            oRela = rela.obtenerRelacionPorOrigenYDestino(idVista, atr['accion_interna'])
            existeRela = False
            if oRela != None :
                id_salida = json.loads(oRela.propiedades)['id_salida']
                existeRela = id_salida == atr['id'] 
            
            if not existeRela:
                listaRelaVisAcc = rela.obtenerRelacionesDirigidasVistaAccion(idVista)

                for r in listaRelaVisAcc:
                    # Eliminamos la relacion anterior.
                    id_salida = json.loads(r.propiedades)['id_salida']
                    if id_salida == atr['id']: 
                        eliminado = rela.eliminarRelacionPorID(r.idRelacion)

                creado1 = rela.crearRelacion(None, TIPO_VISTA_ACCION, json.dumps(propiedades_rela), idVista, atr['accion_interna'], idDiagrama)

                if not creado1 : 
                    creado1 = False
                    break
        else:
            listaRelaVisAcc = rela.obtenerRelacionesDirigidasVistaAccion(idVista)

            for r in listaRelaVisAcc:
                # Eliminamos la relacion anterior.
                id_salida = json.loads(r.propiedades)['id_salida']
                if id_salida == atr['id']: 
                    eliminado = rela.eliminarRelacionPorID(r.idRelacion)


        
        if atr['accion_externa'] != 0:
            # Obtenemos la accion a la cual asociaremos la salida de la vista.
            nd = nodo.obtenerNodoPorID(atr['accion_externa'])

            # Debemos crear un nodo externo para la accion. Pero primero verificamos sino existe ya.
            existe = nodo.obtenerNodoExternoAsociadoAlDiagrama(idDiagrama, nd.idNodo)

            creadoExt1 = True
            if not existe:
                # Si no existe creamos el nodo externo asociado al nodo real.
                creadoExt1 = nodo.crearNodoExterno(nd.nombre, json.dumps({}), idDiagrama, nd.idNodo)

            if creadoExt1:

                # Antes de crear la relacion buscamos si existe.
                existeRela = rela.obtenerRelacionPorOrigenYDestino(idVista, atr['accion_interna'])
            
                if not existeRela:
                    # Creamos la nueva relacion pero antes eliminamos la anterior.
                    listaRelaVisExt = rela.obtenerRelacionesDirigidasVistaExterno(idVista)

                    for r in listaRelaVisExt:
                        # Eliminamos la relacion anterior.
                        id_salida = json.loads(r.propiedades)['id_salida']
                        if id_salida == atr['id']: 
                            eliminado = rela.eliminarRelacionPorID(r.idRelacion)

                    # Obtenemos la relacion externo-accion del otro diagrama.
                    nodoExt = nodo.obtenerNodoExternoAsociadoAlDiagrama(nd.idDiagrama, idVista)
                    
                    if nodoExt != None:
                        listaRelaExtVis = rela.obtenerRelacionesDirigidasExternoVista(nodoExt.idNodo)

                        for r in listaRelaExtVis:
                            if idVista == r.idNodoDestino:
                                eliminado = rela.eliminarRelacionPorID(r.idRelacion)
                    
                    # Obtenemos el nodo recien creado.
                    nodoExt = nodo.obtenerNodoExternoAsociadoAlDiagrama(idDiagrama, nd.idNodo)

                    # Obtenemos la lista de nodos externos del diagrama actual.
                    listaExternosDiag = nodo.obtenerNodosExternoPorDiagrama(idDiagrama)

                    posIni = 80 + len(listaExternosDiag)*60

                    # Establecemos la posicion del nodo.
                    creadoEstiloNodo = eNodo.crearEstiloNodo(idDiagrama, nodoExt.idNodo, json.dumps({"x": 750, "y": posIni}))

                    # Creamos la relacion con el nodo externo creado.
                    propiedades_rela = {"id_salida": atr['id']}
                    creado2 = rela.crearRelacion(None, TIPO_VISTA_EXTERNO, json.dumps(propiedades_rela), idVista, nodoExt.idNodo, idDiagrama)
            
                    if not creado2: 
                        creado2 = False
                        break


                    # Creamos ahora la vista actual en el diagrama de la accion pero como nodo externo.
                    
                    # Verificamos si el nodo externo a crear existe en el otro diagrama.
                    existe = nodo.obtenerNodoExternoAsociadoAlDiagrama(nd.idDiagrama, idVista)

                    creadoExt2 = True
                    if not existe:
                        creadoExt2 = nodo.crearNodoExterno(nombreVista, json.dumps({}), nd.idDiagrama, idVista)

                    if creadoExt2:
                        # Obtenemos el nodo recien creado.
                        nodoExt = nodo.obtenerNodoExternoAsociadoAlDiagrama(nd.idDiagrama, idVista)

                        # Obtenemos la lista de nodos externos del diagrama de la accion.
                        listaExternosDiag = nodo.obtenerNodosExternoPorDiagrama(nd.idDiagrama)

                        posIni = 80 + len(listaExternosDiag)*60

                        # Establecemos la posicion del nodo.
                        creadoEstiloNodo = eNodo.crearEstiloNodo(idDiagrama, nodoExt.idNodo, json.dumps({"x": 750, "y": posIni}))

                        # Creamos la relaccion externo-accion.
                        creado3 = rela.crearRelacion(None, TIPO_ACCION_EXTERNO, json.dumps({}), nodoExt.idNodo, nd.idNodo, nd.idDiagrama)

                        if not creado3:
                            creado3 = False
                            break
        else:
            listaRelaVisExt = rela.obtenerRelacionesDirigidasVistaExterno(idVista)

            for r in listaRelaVisExt:
                # Eliminamos la relacion anterior.
                id_salida = json.loads(r.propiedades)['id_salida']
                if id_salida == atr['id']: 
                    eliminado = rela.eliminarRelacionPorID(r.idRelacion)

            # Obtnemos el nodo externo del diagrama.
            nodoExt = nodo.obtenerNodoExternoAsociadoAlDiagrama(idDiagrama, atr['accion_anterior'])

            if nodoExt != None:
                listaRelaVisExt = rela.obtenerRelacionesPorDestino(nodoExt.idNodo)
                if listaRelaVisExt == []:
                    nodo.eliminarNodoPorId(nodoExt.idNodo)

            # Obtnemos el nodo anterior para saber a que diagrama pertenece.
            nd = nodo.obtenerNodoPorID(atr['accion_anterior'])

            if nd != None:

                nodoExt = nodo.obtenerNodoExternoAsociadoAlDiagrama(nd.idDiagrama, idVista)
                        
                if nodoExt != None:
                    listaRelaciones = rela.obtenerRelacionesDirigidasExternoAccion(nodoExt.idNodo)
                    
                    for r in listaRelaciones:
                        anterior = atr['accion_anterior']  
                        if anterior == r.idNodoDestino:
                            eliminado = rela.eliminarRelacionPorID(r.idRelacion) 

                    listaRelaciones = rela.obtenerRelacionesDirigidasExternoAccion(nodoExt.idNodo)

                    if listaRelaciones == []:
                        nodo.eliminarNodoPorId(nodoExt.idNodo)



    if actualizado and creado1 and creado2 and creado3:
        res = results[0]

    res['label'] = res['label'] + '/' + str(idDiagrama)

    return json.dumps(res)



@elem.route('/elemento/AModificarAccion', methods=['POST'])
def AModificarAccion():
    params  = request.get_json()
    results = [{'label':'/VDiagrama', 'msg':['Accion Modificada']},
               {'label':'/VDiagrama', 'msg':['Error al modificar accion']},]

    # Asignamos el mensaje a mostrar por defecto.
    res = results[1]

    # Obtenemos el id del diagrama al cual pertenece el elemento.
    idDiagrama = int(session['idDiagrama'])

    # Extraemos los parametros.
    idAccion      = params['idNodo']
    nombreAccion  = params['nombre'] 
    rela_internas = params['relaciones_internas']
    rela_externas = params['relaciones_externas']

    anterior = nodo.obtenerNodoPorID(idAccion)

    # Agregamos las nuevas relaciones.

    propiedades = json.loads(anterior.propiedades)
    # propiedades['atributos'] = atributos

    actualizado = nodo.actualizarNodoAccion(idAccion, nombreAccion, json.dumps(propiedades))

    # Obtenemos con quienes esta relacionado.
    lista_relaInternas = rela.obtenerRelacionesDirigidasAccionVista(idAccion)
    lista_relaExternas = rela.obtenerRelacionesDirigidasAccionExterno(idAccion)

    # Creamos las relaciones internas nuevas sino existen previamente.
    creadoRelaInterno = True
    for r in rela_internas:

        # Buscamos si existe una relacion igual a la que se quiere crear.
        existe = False
        for x in lista_relaInternas:
            # Verificamos si a quien realmente representa es al mismo que queremos relacionar.
            existe = r['idVista'] == x.idNodoDestino

            if existe: break

        if not existe:
            creadoAux = creadoRelaInterno
            creadoRelaInterno = rela.crearRelacion(None, TIPO_VISTA_ACCION, json.dumps(propiedades), idAccion, r['idVista'], idDiagrama)
            creadoRelaInterno = creadoAux and creadoRelaInterno


    # Creamos las relaciones externas nuevas sino existen previamente.
    creadoRelaExterno = True
    for r in rela_externas:

        # Buscamos si existe una relacion igual que la que se quiere crear.
        existe = False
        n = None
        for x in lista_relaExternas:
            # Obtenemos el nodo destino.
            n = nodo.obtenerNodoPorID(x.idNodoDestino)
            # Verificamos si a quien realmente representa es al mismo que queremos relacionar.
            existe = r['idVista'] == n.idNodoExterno

            if existe: break

        if not existe:
            # Obtenemos el nodo destino a crear.
            nd = nodo.obtenerNodoPorID(r['idVista'])

            creadoNodoExterno1 = nodo.crearNodoExterno(r['nombre'], json.dumps({}), idDiagrama, r['idVista'])
            
            # Verificamos si el nodo destino tiene representacion en el diagrama al que pertenece la vista.
            encontrado = nodo.obtenerNodoExternoAsociadoAlDiagrama(nd.idDiagrama, idAccion)

            creadoNodoExterno2 = True
            if not encontrado:
                creadoNodoExterno2 = nodo.crearNodoExterno(nombreAccion, json.dumps({}), nd.idDiagrama, idAccion)
            
            creadoRelaExterno = False
            creadoEstiloNodo  = False

            if creadoNodoExterno1 and creadoNodoExterno2:        

                # Obtenemos  los nodo externos recien creados.
                nodoExterno1 = nodo.obtenerNodoExternoAsociadoAlDiagrama(idDiagrama, r['idVista'])
                nodoExterno2 = nodo.obtenerNodoExternoAsociadoAlDiagrama(nd.idDiagrama, idAccion)

                if nodoExterno1 != None and nodoExterno2 != None:
                    # Creamos las relaciones.
                    creadoRelaExterno1 = rela.crearRelacion(None, TIPO_ACCION_EXTERNO, json.dumps(propiedades), idAccion, nodoExterno1.idNodo, idDiagrama)
                    creadoRelaExterno2 = rela.crearRelacion(None, TIPO_VISTA_EXTERNO, json.dumps(propiedades), nodoExterno2.idNodo, r['idVista'], nd.idDiagrama)
                    

                    if creadoRelaExterno1 and creadoRelaExterno2:

                        listaExternosDiag1 = nodo.obtenerNodosExternoPorDiagrama(idDiagrama)
                        listaExternosDiag2 = nodo.obtenerNodosExternoPorDiagrama(nd.idDiagrama)

                        posIni1 = 80 + len(listaExternosDiag1)*60
                        posIni2 = 80 + len(listaExternosDiag2)*60

                        # Establecemos la posicion del nodo.
                        creadoEstiloNodo1 = eNodo.crearEstiloNodo(idDiagrama, nodoExterno1.idNodo, json.dumps({"x": 750, "y": posIni1}))
                        creadoEstiloNodo2 = eNodo.crearEstiloNodo(nd.idDiagrama, nodoExterno2.idNodo, json.dumps({"x": 750, "y": posIni2}))

                        if not creadoEstiloNodo1 and creadoEstiloNodo2:
                            nodo.eliminarNodoPorId(nodoExterno1.idNodo)
                            nodo.eliminarNodoPorId(nodoExterno2.idNodo)
                            r1 = rela.obtenerRelacionPorOrigenYDestino(idAccion,  nodoExterno1.idNodo)
                            r2 = rela.obtenerRelacionPorOrigenYDestino(r['idVista'],  nodoExterno2.idNodo)
                            rela.eliminarRelacionPorID(r1.idRelacion)
                            rela.eliminarRelacionPorID(r2.idRelacion)
                            # Eliminar estilo nodo tambien ###################################################################################################
                    else:
                        nodo.eliminarNodoPorId(nodoExterno1.idNodo)
                        nodo.eliminarNodoPorId(nodoExterno2.idNodo)

            creadoRelaExterno = creadoNodoExterno1 and creadoNodoExterno2 and creadoRelaExterno1 and creadoRelaExterno2 and creadoEstiloNodo1 and creadoEstiloNodo2


    if actualizado and creadoRelaInterno and creadoRelaExterno:
        res = results[0]

    res['label'] = res['label'] + '/' + str(idDiagrama)

    return json.dumps(res)



@elem.route('/elemento/AModificarOperacion', methods=['POST'])
def AModificarOperacion():
    params  = request.get_json()
    results = [{'label':'/VDiagrama', 'msg':['Operación Modificada']},
               {'label':'/VDiagrama', 'msg':['Error al modificar Operación']},]

    # # Asignamos el mensaje a mostrar por defecto.
    res = results[1]

    # Obtenemos el id del diagrama al cual pertenece el elemento.
    idDiagrama = int(session['idDiagrama'])

    # Extraemos los parametros
    idOrigen  = params['idNodo'] 
    idDestino = params['idAccion']
    nombreOp  = params['nombre']

    nodoAnterior = nodo.obtenerNodoPorID(idOrigen)

    propiedades = json.loads(nodoAnterior.propiedades)

    actualizado1 = nodo.actualizarNodoOperacion(idOrigen, nombreOp, json.dumps(propiedades))


    # Obtenemos la relacion actual de la operacion con la accion.
    relaAnterior = rela.obtenerRelacionNoDirigidaOperacionAccion(idOrigen)

    if relaAnterior != None:

        if idDestino == 0: # Eliminamos la relacion existente.
            rela.eliminarRelacionPorID(relaAnterior.idRelacion)
        else:

            if idDestino == relaAnterior.idNodoDestino:
                actualizado2 = True
            else:
                propiedades  = json.loads(relaAnterior.propiedades)
                actualizado2 = rela.actualizarRelacion(relaAnterior.idRelacion, None, TIPO_ACCION_OPERACION, json.dumps(propiedades), idOrigen, idDestino, idDiagrama)
    else:
        actualizado2 = rela.crearRelacion(None, TIPO_ACCION_OPERACION, json.dumps({}), idOrigen, idDestino, idDiagrama)

        if actualizado1 and actualizado2:
            res = results[0]

    res['label'] = res['label'] + '/' + str(idDiagrama)

    return json.dumps(res)



@elem.route('/elemento/AEliminarElemento', methods=['GET'])
def AEliminarElemento():
    params  = request.get_json()

    results = [{'label':'/VDiagrama/1', 'msg':['Diagrama creado']},
               {'label':'/VDiagrama', 'msg':['El nombre del diagrama ya existe']},
               {'label':'/VDiagrama', 'msg':['Error al crear diagrama']},]

    # # Asignamos el mensaje a mostrar por defecto.
    res = results[0]

    # Obtenemos el id del nodo que vamos a eliminar.
    idNodo = int(request.args.get('idNodo',1))

    # Buscamos el tipo de nodo que vamos a eliminar.
    nd = nodo.obtenerNodoPorID(idNodo)

    print('Nodo que eliminaremos', nd.nombre)

    # # Extraemos los parametros
    # nombreDiagrama = params['nombre'] 
    # descDiagrama   = params['descripcion']

    # #Obtenemos el id del diseno al cual pertenece el diagrama.
    # idDiseno = int(session['idDiseno'])

    return json.dumps(res)