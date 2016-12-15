# -*- coding: utf-8 -*-.

# DESCRIPCION: 


# Se importan las librerias necesarias.
from modelo import *

# Declaracion de constantes.
NUM_MIN_ID = 1
TAM_MAX_NOMBRE = 64

TIPO_VISTA_ACCION   = 1
TIPO_ACCION_OPERACION  = 2
TIPO_VISTA_EXTERNO  = 3
TIPO_ACCION_EXTERNO = 4


class Relacion(object):
    """"""


    def crearRelacion(self, nombre, tipo, propiedades, idNodoOrigen, idNodoDestino, idDiagrama):
        """
        """
        if tipo != None and propiedades != None and idNodoOrigen != None and idNodoDestino != None and idDiagrama != None:

            if idDiagrama >= NUM_MIN_ID and idNodoOrigen >= NUM_MIN_ID and idNodoDestino >= NUM_MIN_ID:

                if nombre != None:
                    if len(nombre) > TAM_MAX_NOMBRE:
                        return False
                
                if tipo in [TIPO_VISTA_ACCION, TIPO_ACCION_OPERACION, TIPO_VISTA_EXTERNO, TIPO_ACCION_EXTERNO]:
                    nuevaRelacion = clsRelacion(nombre, tipo, propiedades, idNodoOrigen, idNodoDestino, idDiagrama)
                    db.session.add(nuevaRelacion)
                    db.session.commit()
                    return True
        return False


    def obtenerRelacionPorOrigenYDestino(self, idNodoOrigen, idNodoDestino):
        """"""
        relacion = clsRelacion.query.filter_by(idNodoOrigen=idNodoOrigen, idNodoDestino=idNodoDestino).first()

        return relacion


    def obtenerRelacionesPorDestino(self, idNodoDestino):
        """"""
        relacion = clsRelacion.query.filter_by(idNodoDestino=idNodoDestino).all()

        return relacion    


    def obtenerRelacionesPorOrigen(self, idNodoOrigen):
        """"""
        relacion = clsRelacion.query.filter_by(idNodoOrigen=idNodoOrigen).all()

        return relacion    


    def obtenerRelacionNoDirigidaOperacionAccion(self, idNodoOrigen):
        """"""
        relacion = clsRelacion.query.filter_by(tipo=TIPO_ACCION_OPERACION, idNodoOrigen=idNodoOrigen).first()

        return relacion


    def obtenerRelacionesDirigidasVistaExterno(self, idVista):
        """"""
        relacion = clsRelacion.query.filter_by(tipo=TIPO_VISTA_EXTERNO, idNodoOrigen=idVista).all()

        return relacion


    def obtenerRelacionesDirigidasExternoVista(self, idExterno):
        """"""
        relacion = clsRelacion.query.filter_by(tipo=TIPO_VISTA_EXTERNO, idNodoOrigen=idExterno).all()

        return relacion


    def obtenerRelacionesDirigidasAccionVista(self, idAccion):
        """"""
        relacion = clsRelacion.query.filter_by(tipo=TIPO_VISTA_ACCION, idNodoOrigen=idAccion).all()

        return relacion


    def obtenerRelacionesDirigidasVistaAccion(self, idVista):
        """"""
        relacion = clsRelacion.query.filter_by(tipo=TIPO_VISTA_ACCION, idNodoOrigen=idVista).all()

        return relacion


    def obtenerRelacionesDirigidasAccionExterno(self, idAccion):
        """"""
        relacion = clsRelacion.query.filter_by(tipo=TIPO_ACCION_EXTERNO, idNodoOrigen=idAccion).all()

        return relacion


    def obtenerRelacionesDirigidasExternoAccion(self, idExterno):
        """"""
        relacion = clsRelacion.query.filter_by(tipo=TIPO_ACCION_EXTERNO, idNodoOrigen=idExterno).all()

        return relacion


    def obtenerRelacionesPorDiagrama(self, idDiagrama):
        """"""
        relaciones = clsRelacion.query.filter_by(idDiagrama=idDiagrama).all()

        return relaciones


    def obtenerRelacionesPorTipoYDiagrama(self, tipo, idDiagrama):
        """"""
        relaciones = clsRelacion.query.filter_by(tipo=tipo, idDiagrama=idDiagrama).all()

        return relaciones


    def actualizarRelacion(self, idRelacion, nuevoNombre, nuevoTipo, nuevasPropiedades, nuevoIdNodoOrigen, nuevoIdNodoDestino, nuevoIdDiagrama):
        """"""
        if idRelacion != None and nuevoTipo != None and nuevasPropiedades != None and nuevoIdNodoOrigen != None and nuevoIdNodoDestino != None and nuevoIdDiagrama != None:

            if idRelacion >= NUM_MIN_ID and nuevoIdNodoOrigen >= NUM_MIN_ID and nuevoIdNodoDestino >= NUM_MIN_ID and nuevoIdDiagrama >= NUM_MIN_ID:

                viejaRela = clsRelacion.query.filter_by(idRelacion=idRelacion).first()

                if viejaRela != None:

                    if nuevoNombre != None:
                        if len(nuevoNombre) > TAM_MAX_NOMBRE:
                            return False
                    
                    if nuevoTipo in [TIPO_VISTA_ACCION, TIPO_ACCION_OPERACION, TIPO_VISTA_EXTERNO, TIPO_ACCION_EXTERNO]:
                        viejaRela.nombre        = nuevoNombre
                        viejaRela.tipo          = nuevoTipo
                        viejaRela.propiedades   = nuevasPropiedades
                        viejaRela.idNodoOrigen  = nuevoIdNodoOrigen
                        viejaRela.idNodoDestino = nuevoIdNodoDestino
                        viejaRela.idDiagrama    = nuevoIdDiagrama
                        db.session.commit()
                        return True

        return False


    def eliminarRelacionPorID(self, idRelacion):
        """"""
        if idRelacion != None:

            if idRelacion >= NUM_MIN_ID:

                rela = clsRelacion.query.filter_by(idRelacion=idRelacion).first()

                if rela != None:
                    db.session.delete(rela)
                    db.session.commit()
                    return True

        return False


# FIN CLASE RELACION