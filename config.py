# -*- coding: utf-8 -*-.

# DESCRIPCION: Modulo que permite cargar valores ejemplo en el modelo de datos.


import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	DEBUG   = False
	TESTING = False
	SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_COMMIT_ON_TEARDOWN  = True

	@staticmethod
	def init_app(app):
		pass


class DesarrolloConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'data-dev.sqlite')


class PruebasConfig(Config):
	TESTING = True
	PRESERVE_CONTEXT_ON_EXCEPTION = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'data-test.sqlite')

class ProduccionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'data.sqlite')
	


config = {
	'desarrollo': DesarrolloConfig,
	'pruebas'   : PruebasConfig,
	'produccion': ProduccionConfig,

	'default'   : DesarrolloConfig
}