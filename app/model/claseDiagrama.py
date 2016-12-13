# -*- coding: utf-8 -*-.

# DESCRIPCION: Modulo donde se definen las funciones relacionadas a los 
#              diagramas.


# Se importan las librerias necesarias.
from modelo import *

# Declaracion de constantes.
TAM_MAX_NOMBRE = 64
NUM_MIN_ID = 1


class Diagrama(object):
	""""""

	def crearDiagrama(self, nombre, descripcion, propiedades, idDiseno):
		""""""
		if nombre != None and descripcion != None and propiedades != None and idDiseno != None:

			tamNombre = len(nombre) <= TAM_MAX_NOMBRE
			idDiseno_valido = idDiseno >= NUM_MIN_ID

			if tamNombre and idDiseno_valido:
				nuevoDiagrama = clsDiagrama(nombre, descripcion, propiedades, idDiseno)
				db.session.add(nuevoDiagrama)
				db.session.commit()
				return True

		return False


	def obtenerDiagramaPorID(self, idDiagrama):
		""""""
		existeDiagrama = False

		if idDiagrama != None:

			if idDiagrama >= NUM_MIN_ID:

				existeDiagrama = clsDiagrama.query.filter_by(idDiagrama=idDiagrama).first()

		return existeDiagrama


	def obtenerDiagramasPorDiseno(self, idDiseno):
		""""""
		diagramas = clsDiagrama.query.filter_by(idDiseno=idDiseno).all()

		return diagramas


	def actualizarDiagrama(self, idDiagrama, nuevoNombre, nuevaDescripcion, nuevasPropiedades, nuevoIdDiseno):
		""""""
		if idDiagrama != None:

			if idDiagrama >= NUM_MIN_ID:

				viejoDiagrama = clsDiagrama.query.filter_by(idDiagrama=idDiagrama).first()

				if viejoDiagrama != None:

					if nuevoNombre != None and nuevaDescripcion != None and nuevasPropiedades != None:

						if len(nuevoNombre) <= TAM_MAX_NOMBRE:

							viejoDiagrama.nombre      = nuevoNombre
							viejoDiagrama.descripcion = nuevaDescripcion
							viejoDiagrama.propiedades = nuevasPropiedades
							db.session.commit()

							return True

		return False

	def eliminarDiagrama(self, idDiagrama):
		""""""
		if idDiagrama != None:

			if idDiagrama >= NUM_MIN_ID:

				diagrama = clsDiagrama.query.filter_by(idDiagrama=idDiagrama).first()

				if diagrama != None:
					db.session.delete(diagrama)
					db.session.commit()
					return True

		return False

	# Fin Clase Diagrama