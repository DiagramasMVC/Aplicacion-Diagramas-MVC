# -*- coding: utf-8 -*-.

# DESCRIPCION: Modulo donde se definen las funciones relacionadas al usuario.

import sys
# Ruta que permite utilizar el módulo model.py
sys.path.append('app/model')

# Se importan las librerias necesarias.
from modelo import *

# Declaración de constantes.
TAM_MAX_NOMBREUSR = 16
TAM_MIN_NOMBREUSR = 1
TAM_MAX_NOMBRE    = 64
TAM_MIN_NOMBRE    = 1
TAM_MAX_CORREO    = 64
TAM_MIN_CORREO    = 7
TAM_MAX_CLAVE     = 200
TAM_MIN_CLAVE     = 1
MIN_ID_USUARIO    = 1
 

class Usuario(object):
    """Interfaz que provee funciones relacionadas a los usuarios."""
    
    def crearUsuario(self, nombreUsuario, nombreCompleto, clave, correo):
        """Permite insertar un usuario en la tabla de usuarios."""
        tamNombreUsuario  = TAM_MIN_NOMBREUSR <= len(nombreUsuario)  <= TAM_MAX_NOMBREUSR
        tamNombreCompleto = TAM_MIN_NOMBRE    <= len(nombreCompleto) <= TAM_MAX_NOMBRE 
        tamClave          = TAM_MIN_CLAVE     <= len(clave)          <= TAM_MAX_CLAVE
        tamCorreo         = TAM_MIN_CORREO    <= len(correo)         <= TAM_MAX_CORREO

        if tamNombreUsuario and tamNombreCompleto and tamClave and tamCorreo:
            # Verificamos si el nombre de usuario ya existe.
            usr = clsUsuario.query.filter_by(nombreUsuario=nombreUsuario).first()

            if usr == None: # Insertamos al usuario.
                tmpUsuario = clsUsuario(nombreUsuario, nombreCompleto, clave, correo)
                db.session.add(tmpUsuario)
                db.session.commit()
                return True
        return False



    def obtenerUsuarios(self):
        """Permite obtener todos los usurios de la tabla de usuarios."""
        usuarios = clsUsuario.query.all()
        return usuarios



    def obtenerUsuarioPorID(self, idUsuario):
        """Permite obtener un usuario por su identificador"""
        idValido = idUsuario >= MIN_ID_USUARIO
        usuario  = None

        if idValido:
            usuario = clsUsuario.query.filter_by(idUsuario=idUsuario).first()
        return usuario 



    def obtenerUsuarioPorNombreUsuario(self, nombreUsuario):
        """Permite obtener un usuario por su nombre de usuario."""
        tamNombreUsuario = TAM_MIN_NOMBREUSR <= len(nombreUsuario) <= TAM_MAX_NOMBREUSR 
        usuario = None

        if tamNombreUsuario:
            usuario = clsUsuario.query.filter_by(nombreUsuario=nombreUsuario).first()
        return usuario



    def obtenerUsuariosPorCorreo(self, correo):
        """Permite obtener los usurios registrados con el correo dado."""
        tamCorreo = TAM_MIN_CORREO <= len(correo) <= TAM_MAX_CORREO
        usuarios   = []

        if tamCorreo:
            usuarios = clsUsuario.query.filter_by(correo=correo).all()
        return usuarios



    # Funciones utiles a futuro.
    # def actualizarUsuarioPorID(self, idUsuario):
    #     """"""
    #     pass


    # def actualizarUsuarioPorNombreUsuario(self, nombreUsuario):
    #     """"""
    #     pass
        

    # def eliminarUsuarioPorID(self, idUsuario):
    #     """"""
    #     pass


    # def eliminarUsuarioPorNombreUsuario(self, nombreUsuario):
    #     """"""
    #     pass	