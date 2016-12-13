# -*- coding: utf-8 -*-.

# DESCRIPCION: Modulo donde se definen las funciones relacionadas a la 
#              informacion de presentacion de las relaciones.


# Se importan las librerias necesarias.
from modelo import *

# Declaracion de constantes.
NUM_MIN_ID = 1
TAM_MAX_NOMBRE = 60

TIPO_VISTA     = 1
TIPO_ACCION    = 2
TIPO_OPERACION = 3


class EstiloRelacion(object):
    """Interfaz que provee funciones relacionadas con la informacion de 
       presentacion de las relaciones""" 

    def crearEstiloRelacion(self, idDiagrama, idRelacion, propiedades):
        """Permite insertar un nuevo estilo relacion en la base de datos.
           Esta clase se usa para almacenar la informacion de presentacion.

           Recibe:        
           idDiagrama     -- identificador del diagrama al cual pertenece la relación.
           idNodo         -- identificador de la relación.
           propiedades    -- archivo .json con las propiedades.
    
           Devuelve:
           bool -- confirma si se realizo o no la inserción.
        """
        if idDiagrama != None and idRelacion != None and propiedades != None:

            if idDiagrama >= NUM_MIN_ID and idRelacion >= NUM_MIN_ID:

                nuevoEstiloRelacion = clsEstiloRelacion(idDiagrama, idRelacion, propiedades)
                db.session.add(nuevoEstiloRelacion)
                db.session.commit()
                return True

        return False


    def obtenerEstilosRelacionPorDiagrama(self, idDiagrama):
        """"""
        estilosRelacion = clsEstiloRelacion.query.filter_by(idDiagrama=idDiagrama).all()

        return estilosRelacion


    def obtenerEstiloRelacionPorIdNodo(self, idRelacion):
        """"""
        estilosRelacion = clsEstiloRelacion.query.filter_by(idRelacion=idRelacion).first()

        return estilosNodo 


    def actualizarPropiedadesEstiloRelacion(self, idRelacion, nuevasPropiedades):
        """"""
        if idRelacion != None and nuevasPropiedades != None:

            if idRelacion >= NUM_MIN_ID:

                viejaRelacion = clsEstiloRelacion.query.filter_by(idRelacion=idRelacion).first()

                if viejaRelacion != None:
                    viejaRelacion.propiedades = nuevasPropiedades
                    db.session.commit()
                    return True

        return False

    def eliminarEstiloRelacionAsociadoAUnaRelacion(self, idRelacion):
        """"""
        if idRelacion != None:
            if idRelacion >= NUM_MIN_ID:

                estiloRelacion = clsEstiloRelacion.query.filter_by(idRelacion=idRelacion).first()

                if estiloRelacion != None:
                    db.session.delete(estiloRelacion)
                    db.session.commit()
                    return True

        return False


    def eliminarEstiloRelacionPorID(self, idEstiloRelacion):
        """"""
        if idEstiloRelacion != None:
            if idEstiloRelacion >= NUM_MIN_ID:

                estiloRelacion = clsEstiloRelacion.query.filter_by(idEstiloRelacion=idEstiloRelacion).first()

                if estiloRelacion != None:
                    db.session.delete(estiloRelacion)
                    db.session.commit()
                    return True

        return False