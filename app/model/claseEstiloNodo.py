# -*- coding: utf-8 -*-.

# DESCRIPCION: Modulo donde se definen las funciones relacionadas a los nodos.


# Se importan las librerias necesarias.
from modelo import *

# Declaracion de constantes.
NUM_MIN_ID = 1
TAM_MAX_NOMBRE = 60

TIPO_VISTA     = 1
TIPO_ACCION    = 2
TIPO_OPERACION = 3


class EstiloNodo(object):
    """Interfaz que provee funciones relacionadas con la informacion de 
       presentacion de los nodos""" 

    def crearEstiloNodo(self, idDiagrama, idNodo, propiedades):
        """Permite insertar un nuevo estilo nodo en la base de datos.
           Esta clase se usa para almacenar la informacion de presentacion.

           Recibe:        
           idDiagrama     -- identificador del diagrama al cual pertenece el nodo.
           idNodo         -- identificador del nodo.
           propiedades    -- archivo .json con las propiedades.
    
           Devuelve:
           bool -- confirma si se realizo o no la insercion.
        """
        if idDiagrama != None and idNodo != None and propiedades != None:

            if idDiagrama >= NUM_MIN_ID and idNodo >= NUM_MIN_ID:

                nuevoEstiloNodo = clsEstiloNodo(idDiagrama, idNodo, propiedades)
                db.session.add(nuevoEstiloNodo)
                db.session.commit()
                return True

        return False


    def obtenerEstilosNodoPorDiagrama(self, idDiagrama):
        """"""
        estilosNodo = clsEstiloNodo.query.filter_by(idDiagrama=idDiagrama).all()

        return estilosNodo 

    def obtenerEstiloNodoPorIdNodo(self, idNodo):
        """"""
        estilosNodo = clsEstiloNodo.query.filter_by(idNodo=idNodo).first()

        return estilosNodo 

    def actualizarPropiedadesEstiloNodo(self, idNodo, nuevasPropiedades):
        """"""
        if idNodo != None and nuevasPropiedades != None:

            if idNodo >= NUM_MIN_ID:

                viejoNodo = clsEstiloNodo.query.filter_by(idNodo=idNodo).first()

                if viejoNodo != None:
                    viejoNodo.propiedades = nuevasPropiedades
                    db.session.commit()
                    return True

        return False

    def eliminarEstiloNodoAsociadoAUnNodo(self, idNodo):
        """"""
        if idNodo != None:
            if idNodo >= NUM_MIN_ID:

                estiloNodo = clsEstiloNodo.query.filter_by(idNodo=idNodo).first()

            if estiloNodo != None:
                db.session.delete(estiloNodo)
                db.session.commit()
                return True

        return False