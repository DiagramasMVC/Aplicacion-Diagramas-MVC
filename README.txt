# -*- coding: utf-8 -*-.

# DEPENDENCIAS: es necesario instalarlas para correr la aplicacion.
#	Flask==0.10.1
#	Flask-Migrate==1.1.0
#	Flask-SQLAlchemy==1.0
#	Flask-Script==0.6.6

#	Se puden instalar automaticamente usando:
#	(venv) $ pip freeze >requirements.txt


# PRUEBAS UNITARIAS: para correr todas las pruebas usar
#    python3 base.py test


# MIGRACION: python3 manage.py db upgrade


# EJECUCION: Para ejecutar bajo Linux 
#            (para otros sistemas, por favor consultar la documentacion de Flask)
#            Necesitará tener instalado pip3
#            Si no lo tiene instalado, puede hacerlo ejecutando el comando

sudo apt-get install python3-pip

#            Crear una carpeta aplicaciones

mkdir aplicaciones

#            En una ventana de comandos cambiar a la carpeta principal de la aplicación.

cd aplicaciones

Crear el ambiente virtual

pyvenv-3.4 --without-pip --system-site-packages venv3

#            Descomprimir los archivos de esta distribución

#            Activar el ambiente virtual

source venv3/bin/activate

#            Instalar Flask (La primera vez que lo haga puede que necesite ejecutarlo 
#            con sudo)

pip3 install flask

#            Instalar la gestión de opciones del servidor web  (La primera vez que lo 
#            haga puede que necesite ejecutarlo con sudo)

sudo pip3 install flask-script

#            Ejecutar la aplicación

python base.py runserver

#            El servidor quedará ejecutando indefinidamente.
#            Puede abrir en un navegador la dirección
#            http://127.0.0.1:8000/ para entrar en la aplicación.

#            Para detener el servidor 
#            escribir Ctrl-c en la cónsola en la que ejecuta el servidor.

#            Ejecutar la aplicación

python base.py runserver

#            Si va a utilizar SQLAlchemy verifique que este paquete está instalado. Si no
#            es el caso pruebe ejecutando los siguientes comandos de instalación:

sudo pip3 install SQLAlchemy
sudo pip3 install Flask-SQLAlchemy
sudo pip3 install Flask-Migrate

#            Para verificar si ya están instalados ejecute python3 una consola de 
#            terminal e importe los archivos pertinentes:

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy