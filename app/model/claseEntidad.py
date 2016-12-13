# -*- coding: utf-8 -*-.

# DESCRIPCION: Modulo donde se definen las funciones relacionadas a los 
#              diagramas.


# Se importan las librerias necesarias.
from modelo import *

# Declaracion de constantes.
TAM_MAX_NOMBRE = 64
NUM_MIN_ID = 1


class Entidad(object):
	""""""

	def crearEntidad(self, nombre, propiedades, idDiseno):
		""""""
		if nombre != None and propiedades != None and idDiseno != None:

			tamNombre = len(nombre) <= TAM_MAX_NOMBRE
			idDiseno_valido = idDiseno >= NUM_MIN_ID

			if tamNombre and idDiseno_valido:
				nuevaEntidad = clsEntidad(nombre, propiedades, idDiseno)
				db.session.add(nuevaEntidad)
				db.session.commit()
				return True

		return False


	def obtenerEntidadPorID(self, idEntidad):
		""""""
		existeEntidad = None

		if idEntidad != None:

			if idEntidad >= NUM_MIN_ID:

				existeEntidad = clsEntidad.query.filter_by(idEntidad=idEntidad).first()

		return existeEntidad


	def obtenerEntidadesPorDiseno(self, idDiseno):
		""""""
		entidades = clsEntidad.query.filter_by(idDiseno=idDiseno).all()

		return entidades


	def actualizarEntidad(self, idEntidad, nuevoNombre, idDiseno):
		""""""
		if idEntidad != None:

			if idEntidad >= NUM_MIN_ID:

				viejaEntidad = clsEntidad.query.filter_by(idEntidad=idEntidad).first()

				if viejaEntidad != None:

					if nuevoNombre != None:

						viejaEntidad.nombre = nuevoNombre
						db.session.commit()

						return True
		return False


	def eliminarEntidadPorID(self, idEntidad):
		""""""
		if idEntidad != None:

			if idEntidad >= NUM_MIN_ID:

				#  Obtenemos la entidad que queremos eliminar.
				entidad = clsEntidad.query.filter_by(idEntidad=idEntidad).first()

				if entidad != None:
					db.session.delete(entidad)
					db.session.commit()
					return True

		return False

	# Fin Clase Diagrama