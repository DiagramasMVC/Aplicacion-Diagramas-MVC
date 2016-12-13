# -*- coding: utf-8 -*-.

# DESCRIPCION: Modulo donde se definen las funciones relacionadas a los nodos.


# Se importan las librerias necesarias.
from modelo import *

# Declaracion de constantes.
NUM_MIN_ID = 1
TAM_MAX_NOMBRE = 64

TIPO_VISTA     = 1
TIPO_ACCION    = 2
TIPO_OPERACION = 3
TIPO_EXTERNO   = 4


class Nodo(object):
    """Interfaz que provee funciones relacionadas con los nodos"""


    def crearNodoVista(self, nombre, propiedades, idDiagrama):
        """Permite insertar un nuevo nodo de tipo vista en la base de datos.

           Recibe:
           nombre         -- nombre del nodo a crear.
           propiedades    -- archivo .json con las propiedades.
           idDiagrama     -- identificador del diagrama al cual pertenece el nodo.
    
           Devuelve:
           bool -- confirma si se realizó o no la inserción.
        """
        if nombre != None and propiedades != None and idDiagrama != None:

            if idDiagrama >= NUM_MIN_ID:

                if len(nombre) <= TAM_MAX_NOMBRE:
                    nuevaVista = clsVista(nombre, TIPO_VISTA, propiedades, idDiagrama)
                    db.session.add(nuevaVista)
                    db.session.commit()
                    return True
        return False


    def crearNodoAccion(self, nombre, propiedades, idDiagrama):
        """Permite insertar un nuevo nodo de tipo acción en la base de datos.

           Recibe:
           nombre         -- nombre del nodo a crear.
           propiedades    -- archivo .json con las propiedades.
           idDiagrama     -- identificador del diagrama al cual pertenece el nodo.
    
           Devuelve:
           bool -- confirma si se realizó o no la inserción.
        """
        if nombre != None and propiedades != None and idDiagrama != None:

            if idDiagrama >= NUM_MIN_ID:

                if len(nombre) <= TAM_MAX_NOMBRE:
                    nuevaAccion = clsAccion(nombre, TIPO_ACCION, propiedades, idDiagrama)
                    db.session.add(nuevaAccion)
                    db.session.commit()
                    return True
        return False


    def crearNodoOperacion(self, nombre, propiedades, idDiagrama, idEntidad):
        """Permite insertar un nuevo nodo de tipo operaciño en la base de datos.

           Recibe:
           nombre      -- nombre del nodo a crear.
           propiedades -- archivo .json con las propiedades.
           idDiagrama  -- identificador del diagrama al cual pertenece el nodo.
           idEntidad   -- entidad a la cual esta asociada.
    
           Devuelve:
           bool -- confirma si se realizó o no la inserción.
        """
        if nombre != None and propiedades != None and idDiagrama != None and idEntidad:

            if idDiagrama >= NUM_MIN_ID and idEntidad >= NUM_MIN_ID:

                if len(nombre) <= TAM_MAX_NOMBRE:
                    nuevaOperacion = clsOperacion(nombre, TIPO_OPERACION, propiedades, idDiagrama, idEntidad)
                    db.session.add(nuevaOperacion)
                    db.session.commit()
                    return True
        return False


    def crearNodoExterno(self, nombre, propiedades, idDiagrama, idNodoExt):
        """Permite insertar un nuevo nodo de tipo externo en la base de datos.

           Recibe:
           nombre      -- nombre del nodo a crear.
           propiedades -- archivo .json con las propiedades.
           idDiagrama  -- identificador del diagrama al cual pertenece el nodo.
           idNodoExt   -- nodo al que representa.
    
           Devuelve:
           bool -- confirma si se realizó o no la inserción.
        """
        if nombre != None and propiedades != None and idDiagrama != None and idNodoExt != None:
        
            if idDiagrama >= NUM_MIN_ID and idNodoExt >= NUM_MIN_ID:

                if len(nombre) <= TAM_MAX_NOMBRE:

                    nuevoNodo = clsExterno(nombre, TIPO_EXTERNO, propiedades, idDiagrama, idNodoExt)
                    db.session.add(nuevoNodo)
                    db.session.commit()
                    return True
        return False


    def obtenerNodosPorDiagrama(self, idDiagrama):
        """Permite obtener todos los nodos asociados a un diagrama dado

           Recibe:
           idDiagrama     -- identificador del diagrama al cual pertenecen los nodos.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsNodo. En caso de no existir nodos devuelve 
           lista vacia.
        """
        nodos = clsNodo.query.filter_by(idDiagrama=idDiagrama).all()

        return nodos



    def obtenerNodosVistaPorDiagrama(self, idDiagrama):
        """Permite obtener los nodos de tipo vista almacenados en la base
           de datos para un diagrama dado.
           
           Recibe:
           idDiagrama     -- identificador del diagrama al cual pertenece el nodo.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsVista. En caso de no existir nodos devuelve 
           lista vacia.
        """
        vistas = clsVista.query.filter_by(idDiagrama=idDiagrama).all()

        return vistas


    def obtenerNodosVistaPorDiseno(self, idDiseno):
        """Permite obtener los nodos de tipo vista almacenados en la base
           de datos para un diagrama dado.
           
           Recibe:
           idDiseno    -- identificador del diseno al cual pertenece el nodo.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsVista. En caso de no existir nodos devuelve 
           lista vacia.
        """
        diagramas = clsDiagrama.query.filter_by(idDiseno=idDiseno).all()
       
        vistas = [] 
        for d in diagramas:
            listaVistas = clsVista.query.filter_by(idDiagrama=d.idDiagrama).all()
            vistas += listaVistas

        return vistas


    def obtenerNodosAccionPorDiagrama(self, idDiagrama):
        """Permite obtener los nodos de tipo accion almacenados en la base
           de datos para un diagrama dado.
           
           Recibe:
           idDiagrama     -- identificador del diagrama al cual pertenece el nodo.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsAccion. En caso de no existir nodos devuelve 
           lista vacia.
        """
        acciones = clsAccion.query.filter_by(idDiagrama=idDiagrama).all()

        return acciones


    def obtenerNodosAccionPorDiseno(self, idDiseno):
        """Permite obtener los nodos de tipo accion almacenados en la base
           de datos para un diagrama dado.
           
           Recibe:
           idDiseno     -- identificador del diseno al cual pertenece el nodo.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsAccion. En caso de no existir nodos devuelve 
           lista vacia.
        """
        diagramas = clsDiagrama.query.filter_by(idDiseno=idDiseno).all()
       
        acciones = [] 
        for d in diagramas:
            listaAcciones = clsAccion.query.filter_by(idDiagrama=d.idDiagrama).all()
            acciones += listaAcciones

        return acciones


    def obtenerNodosOperacionPorDiagrama(self, idDiagrama):
        """Permite obtener los nodos de tipo operacion almacenados en la base
           de datos para un diagrama dado.
           
           Recibe:
           idDiagrama     -- identificador del diagrama al cual pertenece el nodo.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsOperacion. En caso de no existir nodos devuelve 
           lista vacia.
        """
        operaciones = clsOperacion.query.filter_by(idDiagrama=idDiagrama).all()

        return operaciones


    def obtenerNodosOperacionPorDiagramaYEntidad(self, idDiagrama, idEntidad):
        """Permite obtener los nodos de tipo operacion almecenados en la base de datos 
           para un diagrama y entida dados

           Recibe:
           Ningun argumento.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsOperacion. En caso de no existir nodos devuelve 
           lista vacia."""

        operaciones = clsOperacion.query.filter_by(idDiagrama=idDiagrama, idEntidad=idEntidad).all()

        return operaciones


    def obtenerNodosExternoPorDiagrama(self, idDiagrama):
        """Permite obtener los nodos de tipo externo almacenados en la base
           de datos para un diagrama dado.
           
           Recibe:
           idDiagrama     -- identificador del diagrama al cual pertenece el nodo.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsExterno. En caso de no existir nodos devuelve 
           lista vacia.
        """
        externos = clsExterno.query.filter_by(idDiagrama=idDiagrama).all()

        return externos


    def obtenerNodosExternosPorIdDelNodoReal(self, idNodoReal):
        """Permite obtener los nodos externos de distintos diagramas asociado a un 
           id de nodo"""
        externos = clsExterno.query.filter_by(idNodoExterno=idNodoReal).all()

        return externos


    def obtenerNodoExternoAsociadoAlDiagrama(self, idDiagrama, idNodoReal):
        """Permite obtener el nodo externo de un diagrama dado que representa a
           un nodo de otro diagrama"""
        nodo = clsExterno.query.filter_by(idDiagrama=idDiagrama, idNodoExterno=idNodoReal).first()

        return nodo
    

    def obtenerNodoPorID(self, idNodo):
        """Permite obtener nodos por su identificador único.
           
           Recibe:
           idNOdo -- identificador del nodo a buscar.

           Devuelve:
           <idNodo, nombre, tipo, propiedades, idDiagrama>] -- tuplas
           correspondiente a clsNodo. En caso de no existir nodo devuelve 
           None.
        """
        nodo = clsNodo.query.filter_by(idNodo=idNodo).first()

        return nodo


    def obtenerNodosPorDiagrama(self, idDiagrama):
        """Permite obtener todos los nodos que componen un diagrama.

           Recibe:
           idDiagrama -- identificador del diagrama al cual pertenece los nodos.

           Devuelve:
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsNodo. En caso de no existir disenos devuelve 
           lista vacia.
        """
        nodos = clsNodo.query.filter_by(idDiagrama=idDiagrama).all()

        return nodos


    def obtenerNodosPorDiseno(self, idDiseno):
        """Permite obtener todos los nodos asociados a un diseno.

           Recibe:
           idDiseno -- identificador del diseno al cual pertenecen los nodos.

           Devuelve:
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsNodo. En caso de no existir disenos devuelve 
           lista vacia.
        """
        nodos  = []
        diseno = clsDiseno.query.filter_by(idDiseno=idDiseno).first()

        if diseno != None:

            diagramas   = clsDiagrama.query.filter_by(idDiseno=idDiseno).all()

            for d in diagramas:
                nodos = nodos + clsNodo.query.filter_by(idDiagrama=d.idDiagrama).all()

        return nodos


    def actualizarNodoVista(self, idNodo, nuevoNombre, nuevasPropiedades):
        """Permite actualizar el valor de los campos de un nodo vista.
            
           Recibe:
           idNodo            -- identificador del nodo en la tabla de nodos.
           nuevoNombre       -- nuevo nombre a actualizar.
           nuevasPropiedades -- archivo .json con las propiedades a actualizar.
    
           Devuelve:
           bool -- confirma si se actualizo o no el elemento.
        """
        if idNodo != None and nuevoNombre != None and nuevasPropiedades != None:

          if idNodo >= NUM_MIN_ID:

            viejoNodo = clsNodo.query.filter_by(idNodo=idNodo).first()

            if viejoNodo != None:

                if len(nuevoNombre) <= TAM_MAX_NOMBRE:
                
                  viejoNodo.nombre      = nuevoNombre
                  viejoNodo.nuevoTipo   = TIPO_VISTA
                  viejoNodo.propiedades = nuevasPropiedades
                  db.session.commit()
                  return True

        return False


    def actualizarNodoAccion(self, idNodo, nuevoNombre, nuevasPropiedades):
        """Permite actualizar el valor de los campos de un nodo vista.
            
           Recibe:
           idNodo            -- identificador del nodo en la tabla de nodos.
           nuevoNombre       -- nuevo nombre a actualizar.
           nuevasPropiedades -- archivo .json con las propiedades a actualizar.
    
           Devuelve:
           bool -- confirma si se actualizo o no el elemento.
        """
        if idNodo != None and nuevoNombre != None and nuevasPropiedades != None:

          if idNodo >= NUM_MIN_ID:

            viejoNodo = clsNodo.query.filter_by(idNodo=idNodo).first()

            if viejoNodo != None:

                if len(nuevoNombre) <= TAM_MAX_NOMBRE:
                
                  viejoNodo.nombre      = nuevoNombre
                  viejoNodo.nuevoTipo   = TIPO_ACCION
                  viejoNodo.propiedades = nuevasPropiedades
                  db.session.commit()
                  return True

        return False


    def actualizarNodoOperacion(self, idNodo, nuevoNombre, nuevasPropiedades, nuevoidEntidad):
        """"""
        if idNodo != None and nuevoNombre != None and nuevasPropiedades != None and nuevoidEntidad != None:

          if idNodo >= NUM_MIN_ID and nuevoidEntidad >= NUM_MIN_ID:

            viejoNodo = clsNodo.query.filter_by(idNodo=idNodo).first()

            if viejoNodo != None:

                if len(nuevoNombre) <= TAM_MAX_NOMBRE:
                
                  viejoNodo.nombre      = nuevoNombre
                  viejoNodo.nuevoTipo   = TIPO_OPERACION
                  viejoNodo.propiedades = nuevasPropiedades
                  viejoNodo.idEntidad   = nuevoidEntidad
                  db.session.commit()
                  return True

        return False


    def actualizarNodoExterno(self, idNodo, nuevoNombre, nuevasPropiedades, nuevoIdDiagrama, nuevoIdNodoExt):
        """Permite actualizar el valor de los campos de un nodo externo.
            
           Recibe:
           idNodo            -- identificador del nodo en la tabla de nodos.
           nuevoNombre       -- nuevo nombre a actualizar.
           nuevasPropiedades -- archivo .json con las propiedades a actualizar.
           nuevoIdDiagrama   -- identificador del diagrama al cual pertenece el nodo.
           nuevoIdNodoExt    -- identificar del nuevo nodo al que representa.
    
           Devuelve:
           bool -- confirma si se actualizo o no el elemento.
        """
        if idNodo != None and nuevoNombre != None and nuevasPropiedades != None and nuevoIdDiagrama != None and nuevoIdNodoExt != None:

          if idNodo >= NUM_MIN_ID:

            viejoNodo = clsExterno.query.filter_by(idNodo=idNodo).first()

            if viejoNodo != None:

                if len(nuevoNombre) <= TAM_MAX_NOMBRE:
                
                  viejoNodo.nombre        = nuevoNombre
                  viejoNodo.propiedades   = nuevasPropiedades
                  viejoNodo.idDiagrama    = nuevoIdDiagrama
                  viejoNodo.idNodoExterno = nuevoIdNodoExt
                  db.session.commit()
                  return True

        return False


    def eliminarNodoPorId(self, idNodo):
        """Permite eliminar un nodo almacenado
           
               Recibe:
               idNodo -- identificador del nodo en la tabla de nodos.

               Devuelve:
               bool -- confirma si se elimino o no el elemento.
        """
        if idNodo != None:

          if idNodo >= NUM_MIN_ID:

            nodo = clsNodo.query.filter_by(idNodo=idNodo).first()

            if nodo != None:
                db.session.delete(nodo)
                db.session.commit()
                return True

        return False