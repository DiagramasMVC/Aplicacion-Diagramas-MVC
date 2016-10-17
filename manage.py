# -*- coding: utf-8 -*-.

# DESCRIPCION: Modulo que permite cargar valores ejemplo en el modelo de datos.

import os

from app           import create_app, db
from app.model     import *
from flask_script  import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def test():
	'''Corre las pruebas unitarias.'''
	import unittest
	pruebas = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(pruebas)


if __name__ == '__main__':
	manager.run()