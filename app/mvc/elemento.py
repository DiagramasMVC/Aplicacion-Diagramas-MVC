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

    # Asignamos el mensaje a mostrar por defecto.
    res = results[1]

    # Obtenemos el id del diagrama y el diseño al cual pertenece el elemento.
    idDiagrama = int(session['idDiagrama'])
    idDiseno   = int(request.args.get('idDiseno',1))

    # Extraemos los parametros.
    idVista     = params['idNodo']
    nombreVista = params['nombre'] 
    atributos   = params['atributos']
    atributos_elim = params['atributos_eliminar']

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
            resultado   = nodo.actualizarNodoExterno(nd.idNodo, nombreVista, json.dumps(propiedades), nd.idDiagrama, idVista)

    # Eliminamos los atributos con sus relaciones que el usuario elimino.
    for a in atributos_elim:
        # Eliminamos la accion interna
        if a['accion_interna'] != 0:
            oRela = rela.obtenerRelacionesDirigidasVistaAccion(idVista)
            
            for r in oRela:
                if r.idNodoDestino == a['accion_interna']:
                    rela.eliminarRelacionPorID(r.idRelacion)

        if a['accion_externa'] != 0:
            # Obtenemos el nodo destino. 
            nd = nodo.obtenerNodoPorID(a['accion_externa'])

            if nd != None:
                # Obtenemos los nodos externos involucrados.
                nodoExt2 = nodo.obtenerNodoExternoAsociadoAlDiagrama(nd.idDiagrama, idVista)
                nodoExt1 = nodo.obtenerNodoExternoAsociadoAlDiagrama(idDiagrama, nd.idNodo)

                oRela1 = rela.obtenerRelacionesDirigidasVistaExterno(idVista)
                oRela2 = rela.obtenerRelacionesDirigidasExternoAccion(nodoExt2.idNodo)

                for r in oRela1:
                    if r.idNodoDestino == nodoExt1.idNodo:
                        rela.eliminarRelacionPorID(r.idRelacion)

                for r in oRela2:
                    if r.idNodoDestino == nd.idNodo:
                        rela.eliminarRelacionPorID(r.idRelacion)

                # Verificamos si podemos eliminar los nodos.

                # Para nodoExt1 buscamos si quedan relaciones con el.
                result1 = rela.obtenerRelacionesDirigidasVistaExterno(idVista)
                result2 = rela.obtenerRelacionesDirigidasExternoVista(nodoExt1.idNodo)

                hay = False
                for r in result1:
                    result = r.idNodoDestino == nodoExt1.idNodo
                    if result == True:
                        hay = True
                        break
                
                if not hay and result2 == []:
                    eliminado = nodo.eliminarNodoPorId(nodoExt1.idNodo)
            
                # Para nodoExt2 buscamos si quedan relaciones con el.
                result1 = rela.obtenerRelacionesDirigidasAccionExterno(nd.idNodo)
                result2 = rela.obtenerRelacionesDirigidasExternoAccion(nodoExt2.idNodo)
            
                hay = False
                for r in result1:
                    result = r.idNodoDestino == nodoExt2.idNodo
                    if result == True:
                        hay = True
                        break

                if not hay and result2 == []:
                    eliminado = nodo.eliminarNodoPorId(nodoExt2.idNodo)



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
                existeRela = rela.obtenerRelacionPorOrigenYDestino(idVista, atr['accion_externa'])
            
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
                    eNodo.eliminarEstiloNodoAsociadoAUnNodo(nodoExt.idNodo)

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
                        eNodo.eliminarEstiloNodoAsociadoAUnNodo(nodoExt.idNodo)

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
    idDiseno   = int(request.args.get('idDiseno',1))

    # Extraemos los parametros.
    idAccion      = params['idNodo']
    nombreAccion  = params['nombre'] 
    rela_internas = params['relaciones_internas']
    rela_externas = params['relaciones_externas']
    elim_internas = params['rela_internas_eliminar']
    elim_externas = params['rela_externas_eliminar']

    anterior = nodo.obtenerNodoPorID(idAccion)

    # Agregamos las nuevas relaciones.

    propiedades = json.loads(anterior.propiedades)

    actualizado = nodo.actualizarNodoAccion(idAccion, nombreAccion, json.dumps(propiedades))

    # Actualizamos los nodos externos asociados a la accion actual.
    listaDiagramas = dia.obtenerDiagramasPorDiseno(idDiseno)

    for d in listaDiagramas:
        nd = nodo.obtenerNodoExternoAsociadoAlDiagrama(d.idDiagrama, idAccion)

        # Si existe actualizamos el nodo externo.
        if nd != None:
            propiedades = json.loads(nd.propiedades)
            resultado = nodo.actualizarNodoExterno(nd.idNodo, nombreAccion, json.dumps(propiedades), nd.idDiagrama, idAccion)

    creado1 = True
    creado2 = True
    creado3 = True

    # Buscamos que en la lista de relaciones a elimanr no este ninguna que se quiera agregar.
    rela_int_elim = []
    for i in elim_internas:
        esta = False
        for j in rela_internas:
            if i == j['idVista']:
                esta = True
                break
        if not esta:
            rela_int_elim.append(i)

    rela_ext_elim = []
    for i in elim_externas:
        esta = False
        for j in rela_externas:
            if i == j['idVista']:
                esta = True
                break
        if not esta:
            rela_ext_elim.append(i)


    # Eliminamos las relaciones internas borradas por el usuario.
    for idV in rela_int_elim:
        relacion  = rela.obtenerRelacionPorOrigenYDestino(idAccion,idV)

        if relacion != None:
            eliminado = rela.eliminarRelacionPorID(relacion.idRelacion)


    # Creamos las nuevas relaciones internas.
    for r in rela_internas:
        #  Buscamos si la relacion no existe.
        oRela = rela.obtenerRelacionPorOrigenYDestino(idAccion, r['idVista'])

        if oRela == None:
            creado1 = rela.crearRelacion(None, TIPO_VISTA_ACCION, json.dumps({}), idAccion, r['idVista'], idDiagrama)
            
        if not creado1:
            creado1 = False
            break


    # Eliminamos las relaciones externas borradas por el usuario.
    for idV in rela_ext_elim:
        # Buscamos el nodo externo asociado al diagrama actual.
        nodoExt1 =  nodo.obtenerNodoExternoAsociadoAlDiagrama(idDiagrama, idV)

        # Buscamos el nodo vista para saber a cual diagrama pertenece.
        nd = nodo.obtenerNodoPorID(idV)

        # Buscamos el nodo externo asociado a la accion en el otro diagrama.
        nodoExt2 = nodo.obtenerNodoExternoAsociadoAlDiagrama(nd.idDiagrama, idAccion)

        if nodoExt1 and nodoExt2:
            # Eliminamos la relacion entre la accion y el externo del diagrama actual.
            relacion  = rela.obtenerRelacionPorOrigenYDestino(idAccion,nodoExt1.idNodo)
            eliminado = rela.eliminarRelacionPorID(relacion.idRelacion)

            # Eliminamos la relacion entre el externo y la vista del otro diagrama.
            relacion  = rela.obtenerRelacionPorOrigenYDestino(nodoExt2.idNodo, idV)
            eliminado = rela.eliminarRelacionPorID(relacion.idRelacion)


            # Verificamos si es posible eliminar los nodos externos.

            # Para nodoExt1 buscamos si quedan relaciones con el.
            result1 = rela.obtenerRelacionesDirigidasAccionExterno(idAccion)
            result2 = rela.obtenerRelacionesDirigidasExternoAccion(nodoExt1.idNodo)

            hay = False
            for r in result1:
                result = r.idNodoDestino == nodoExt1.idNodo
                if result == True:
                    hay = True
                    break
                
            if not hay and result2 == []:
                eliminado = nodo.eliminarNodoPorId(nodoExt1.idNodo)
            
            #  Para nodoExter2 buscamos si quedan relaciones con el.
            result1 = rela.obtenerRelacionesDirigidasVistaExterno(idV)
            result2 = rela.obtenerRelacionesDirigidasExternoVista(nodoExt2.idNodo)
            
            hay = False
            for r in result1:
                result = r.idNodoDestino == nodoExt2.idNodo
                if result == True:
                    hay = True
                    break

            if not hay and result2 == []:
                eliminado = nodo.eliminarNodoPorId(nodoExt2.idNodo)
            

    # Creamos las nuevas relaciones externas.
    for r in rela_externas: 
        # Obtenemos la vista a la cual asociaremos la salida de la accion.
        nd = nodo.obtenerNodoPorID(r['nodo_real'])

        # Debemos crear un nodo externo para la vista. Pero primero verificamos sino existe ya.
        nodoExt1 = nodo.obtenerNodoExternoAsociadoAlDiagrama(idDiagrama, nd.idNodo)

        creadoExt1 = True
        if not nodoExt1:
            # Si no existe creamos el nodo externo asociado al nodo real.
            creadoExt1 = nodo.crearNodoExterno(nd.nombre, json.dumps({}), idDiagrama, nd.idNodo)

        if creadoExt1:
            # Obtenemos nuevamente el nodo que creamos desde cero.
            nodoExt1 = nodo.obtenerNodoExternoAsociadoAlDiagrama(idDiagrama, nd.idNodo)

            # Antes de crear la relacion buscamos si existe.
            existeRela = rela.obtenerRelacionPorOrigenYDestino(idAccion, nodoExt1.idNodo)

            if not existeRela:
                # Obtenemos la lista de nodos externos del diagrama actual.
                listaExternosDiag = nodo.obtenerNodosExternoPorDiagrama(idDiagrama)

                posIni = 80 + len(listaExternosDiag)*30

                # Establecemos la posicion del nodo.
                creadoEstiloNodo = eNodo.crearEstiloNodo(idDiagrama, nodoExt1.idNodo, json.dumps({"x": 750, "y": posIni}))
            
                # Creamos la relacion con el nodo externo creado.
                creado2 = rela.crearRelacion(None, TIPO_ACCION_EXTERNO, json.dumps({}), idAccion, nodoExt1.idNodo, idDiagrama)

            if not creado2:
                creado2 = False
                elim_nodo       = nodo.eliminarNodoPorId(nodoExt1.idNodo)
                elim_estiloNodo = eNodo.eliminarEstiloNodoAsociadoAUnNodo(nodoExt1.idNodo)
                break

        # Creamos ahora la accion actual en el diagrama de la vista pero como nodo externo.
        
        # Verificamos si el nodo externo a crear existe en el otro diagrama.
        nodoExt2 = nodo.obtenerNodoExternoAsociadoAlDiagrama(nd.idDiagrama, idAccion)

        creadoExt2 = True
        if not nodoExt2:
            creadoExt2 = nodo.crearNodoExterno(nombreAccion, json.dumps({}), nd.idDiagrama, idAccion)

        if creadoExt2:
            # Obtenemos el nodo recien creado.
            nodoExt2 = nodo.obtenerNodoExternoAsociadoAlDiagrama(nd.idDiagrama, idAccion)

            # Antes de crear la relacion buscamos si existe.
            existeRela = rela.obtenerRelacionPorOrigenYDestino(nodoExt2.idNodo, nd.idNodo)

            if not existeRela:
                # Obtenemos la lista de nodos externos del diagrama de la vista.
                listaExternosDiag = nodo.obtenerNodosExternoPorDiagrama(nd.idDiagrama)

                posIni = 80 + len(listaExternosDiag)*30

                # Establecemos la posicion del nodo.
                creadoEstiloNodo = eNodo.crearEstiloNodo(idDiagrama, nodoExt2.idNodo, json.dumps({"x": 750, "y": posIni}))
                
                # Creamos la relaccion externo-vista.
                creado3 = rela.crearRelacion(None, TIPO_VISTA_EXTERNO, json.dumps({}), nodoExt2.idNodo, nd.idNodo, nd.idDiagrama)

            if not creado3:
                creado3 = False
                elim_nodo       = nodo.eliminarNodoPorId(nodoExt2.idNodo)
                elim_estiloNodo = eNodo.eliminarEstiloNodoAsociadoAUnNodo(nodoExt2.idNodo)
                break

    if actualizado and creado1 and creado2 and creado3:
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

    results = [{'label':'/VDiagrama', 'msg':['Elemento eliminado.']},
               {'label':'/VDiagrama', 'msg':['Error al eliminar elemento']},]

    # # Asignamos el mensaje a mostrar por defecto.
    res = results[1]

    # Obtenemos el id del nodo que vamos a eliminar.
    idNodo = int(request.args.get('idNodo',1))
    idDiagrama= int(session['idDiagrama'])

    # Buscamos el tipo de nodo que vamos a eliminar.
    nd = nodo.obtenerNodoPorID(idNodo)
    eliminado = True

    if nd.tipo == TIPO_VISTA:
        pass
    elif nd.tipo == TIPO_ACCION:
        pass
    elif nd.tipo == TIPO_OPERACION:
        relacion = rela.obtenerRelacionNoDirigidaOperacionAccion(nd.idNodo)

        if relacion != None:
            rela_elim = rela.eliminarRelacionPorID(relacion.idRelacion)

            if rela_elim:
                eliminado = eNodo.eliminarEstiloNodoAsociadoAUnNodo(nd.idNodo)
                eliminado = nodo.eliminarNodoPorId(nd.idNodo)

    if eliminado: 
        res = results[0]

    res['label'] = res['label'] + '/' + str(idDiagrama)

    return json.dumps(res)