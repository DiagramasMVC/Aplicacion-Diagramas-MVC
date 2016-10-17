# -*- coding: utf-8 -*-.

# DESCRIPCION: Pruebas unitarias de la aplicacion funcionando.

# Se importan las librerias necesarias.
import unittest

from flask import current_app
from app   import create_app, db


class PruebaAplicacion(unittest.TestCase):
	'''Pruebas unitarias de la aplicacion funcionando'''

	def setUp(self):
	    self.app = create_app('pruebas')
	    self.app_context = self.app.app_context()
	    self.app_context.push()
	    db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()



	def testAplicacionExiste(self):
		self.assertFalse(current_app is None)

	def testAplicacionProbandose(self):
		self.assertTrue(current_app.config['TESTING'])