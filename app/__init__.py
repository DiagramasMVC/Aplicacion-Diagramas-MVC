# -*- coding: utf-8 -*-.

# DESCRIPCION: Paquete de construccion de la aplicacion.

from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from config           import config

db = SQLAlchemy()

def create_app(nombre_config):
	'''Funcion factory que retorna una instancia de la aplicacion acorde al
	   modo que indique nombre_config (desarrollador, produccion, pruebas)
	'''
	app = Flask(__name__)
	app.config.from_object(config[nombre_config]) #Importa la configuracion adecuada.
	config[nombre_config].init_app(app)
	db.init_app(app)

	return app
