# -*- coding: utf-8 -*-.

# DESCRIPCION: Modulo donde se definen las funciones relacionadas a los nodos.


# Se importan las librerias necesarias.
from modelo import *

# Declaracion de constantes.
NUM_MIN_ID = 1
TAM_MAX_NOMBRE = 60


class Nodo(object):
    """Interfaz que provee funciones relacionadas con los nodos"""
 

    def crearNodo(self, nombre, tipo, propiedades, idDiagrama):
        """Permite insertar un nuevo nodo en la base de datos.

           Recibe:
           nombre         -- nombre del nodo a crear.
           propiedades    -- archivo .json con las propiedades.
           idDiagrama     -- identificador del diagrama al cual pertenece el nodo.
    
           Devuelve:
           bool -- confirma si se realizo o no la insercion.
        """
        if nombre != None and tipo != None and propiedades != None and idDiagrama != None:

            tipo = tipo.lower()

            if idDiagrama >= NUM_MIN_ID:

                if len(nombre) <= TAM_MAX_NOMBRE:

                    if tipo == 'vista':
                        nuevoNodo = clsVista(nombre, tipo, propiedades, idDiagrama) 
                    elif tipo == 'accion':
                        nuevoNodo = clsAccion(nombre, tipo, propiedades, idDiagrama)
                    elif tipo == 'operacion':
                        nuevoNodo = clsOperacion(nombre, tipo, propiedades, idDiagrama)   
                    else:
                        nuevoNodo = clsNodo(nombre, tipo, propiedades, idDiagrama)
                    
                    db.session.add(nuevoNodo)
                    db.session.commit()
                    return True

        return False


    def crearNodoOperacion(self, nombre, propiedades, idDiagrama, idEntidad):
        pass


    def crearNodoExterno(self, nombre, propiedades, idDiagrama, idNodoExt):
        """Permite insertar un nuevo nodo de tipo externo en la base de datos.

           Recibe:
           nombre      -- nombre del nodo a crear.
           propiedades -- archivo .json con las propiedades.
           idDiagrama  -- identificador del diagrama al cual pertenece el nodo.
           idNodoExt   -- nodo al que representa.
    
           Devuelve:
           bool -- confirma si se realizo o no la insercion.
        """
        tipo = 'externo'

        if nombre != None and propiedades != None and idDiagrama != None and idNodoExt != None:
        
            if idDiagrama >= NUM_MIN_ID and idNodoExt >= NUM_MIN_ID:

                if len(nombre) <= TAM_MAX_NOMBRE:

                    nuevoNodo = clsExterno(nombre, tipo, propiedades, idDiagrama, idNodoExt)
                    db.session.add(nuevoNodo)
                    db.session.commit()
                    return True

        return False


    def obtenerNodos(self):
        """Permite obtener todos los nodos almacenados en la base de datos.
           
           Recibe:
           Ningun argumento.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsNodo. En caso de no existir nodos devuelve 
           lista vacia.
        """
        nodos = clsNodo.query.all()

        return nodos


    def obtenerNodosVista(self):
        """Permite obtener todos los nodos de tipo vista almacenados en la base
           de datos.
           
           Recibe:
           Ningun argumento.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsVista. En caso de no existir nodos devuelve 
           lista vacia.
        """
        vistas = clsVista.query.all()

        return vistas


    def obtenerNodosAccion(self):
        """Permite obtener todos los nodos de tipo accion almacenados en la base
           de datos.
           
           Recibe:
           Ningun argumento.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsAccion. En caso de no existir nodos devuelve 
           lista vacia.
        """
        acciones = clsAccion.query.all()

        return acciones


    def obtenerNodosOperacion(self):
        """Permite obtener todos los nodos de tipo operacion almacenados en la base
           de datos.
           
           Recibe:
           Ningun argumento.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsOperacion. En caso de no existir nodos devuelve 
           lista vacia.
        """
        operaciones = clsOperacion.query.all()

        return operaciones


    def obtenerNodosExterno(self):
        """Permite obtener todos los nodos de tipo externo almacenados en la base
           de datos.
           
           Recibe:
           Ningun argumento.

           Devuelve: 
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsExterno. En caso de no existir nodos devuelve 
           lista vacia.
        """
        externos = clsExterno.query.all()

        return externos


    def existeNodo(self, idNodo):
        """Permite saber si un nodo se encuentra almacenado en la base de 
           datos o no.

           Recibe:
           idNodo -- identificador del nodo en la tabla nodos.

           Devuelve:
           bool -- confirma si existe o no el elemento.
        """
        existeNodo = None

        if idNodo != None:

            if idNodo >= NUM_MIN_ID:
                existeNodo = clsNodo.query.filter_by(idNodo=idNodo).first()

        return (existeNodo != None)
    

    def obtenerNodoPorID(self):
        """"""
        pass


    def obtenerNodosPorNombre(self, nombre):
        """Permite obtener nodos por su nombre. El nombre no es unico.
           
           Recibe:
           nombre -- nombre del nodo a buscar.

           Devuelve:
           [<idNodo, nombre, tipo, propiedades, idDiagrama>] -- lista de tuplas 
           correspondientes a clsNodo. En caso de no existir disenos devuelve 
           lista vacia.
        """
        nodos = clsNodo.query.filter_by(nombre=nombre).all()

        return nodos  


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


    def actualizarNodo(self, idNodo, nuevoNombre, nuevoTipo, nuevasPropiedades, nuevoIdDiagrama):
        """Permite actualizar el valor de los campos de un nodo.
            
           Recibe:
           idNodo            -- identificador del nodo en la tabla de nodos.
           nuevoNombre       -- nuevo nombre a actualizar.
           nuevoTipo         -- nuevo tipo a actualizar.
           nuevasPropiedades -- archivo .json con las propiedades a actualizar.
           nuevoIdDiagrama   -- identificador del diagrama al cual pertenece el nodo.
    
           Devuelve:
           bool -- confirma si se actualizo o no el elemento.
        """
        if idNodo != None and nuevoNombre != None and nuevoTipo != None and nuevasPropiedades != None and nuevoIdDiagrama != None:

          if idNodo >= NUM_MIN_ID:

            viejoNodo = clsNodo.query.filter_by(idNodo=idNodo).first()

            if viejoNodo != None:

                if len(nuevoNombre) <= TAM_MAX_NOMBRE:
                
                  viejoNodo.nombre      = nuevoNombre
                  viejoNodo.nuevoTipo   = nuevoTipo
                  viejoNodo.propiedades = nuevasPropiedades
                  viejoNodo.nuevoIdDiagrama = nuevoIdDiagrama
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
                
                  viejoNodo.nombre      = nuevoNombre
                  viejoNodo.propiedades = nuevasPropiedades
                  viejoNodo.nuevoIdDiagrama = nuevoIdDiagrama
                  viejoNodo.nuevoIdNodoExt  = nuevoIdNodoExt
                  db.session.commit()
                  return True

        return False


    def eliminarNodo(self, idNodo):
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