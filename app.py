# -*- coding: utf-8 -*-.

# import os

# from app           import create_app, db
from flask         import Flask, request, session
# from flask_migrate import Migrate, MigrateCommand
from flask_script  import Manager, Server
from random        import SystemRandom
from datetime      import timedelta
# from app.model.modelo import *

# app     = create_app('default')
app     = Flask(__name__)
manager = Manager(app)
# migrate = Migrate(app, db)

# manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = False,
    host = '0.0.0.0', port = 8000)
)


@app.before_request
def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=45)
        session.modified = True


@app.route('/')
def index():
    return app.send_static_file('index.html')


# Importamos los blueprintes que permitieron modularizar el codigo en 
# distintas archivos.
from app.mvc.identificar import ident
app.register_blueprint(ident)
from app.mvc.diseno import dise
app.register_blueprint(dise)
from app.mvc.entidad import ent
app.register_blueprint(ent)
from app.mvc.diagrama import diag
app.register_blueprint(diag)
from app.mvc.elemento import elem
app.register_blueprint(elem)


# @manager.command
# def test():
# 	'''Corre las pruebas unitarias.'''
# 	import unittest
# 	pruebas = unittest.TestLoader().discover('tests')
# 	unittest.TextTestRunner(verbosity=2).run(pruebas)


if __name__ == '__main__':
	app.config.update(
		SECRET_KEY = repr(SystemRandom().random())
	)
	manager.run()
