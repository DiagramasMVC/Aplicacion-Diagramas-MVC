# -*- coding: utf-8 -*-.

# DESCRIPCION: Modulo que permite cargar valores ejemplo en el modelo de datos.
#

# Se importan las librerias necesarias.
import os
import sys

from modelo import *

sys.path.append('../../')
from flask import current_app
from app   import create_app, db


# Configuracion de la base de datos de prueba.
app = create_app('pruebas')
app_context = app.app_context()
app_context.push()
db.drop_all()
db.create_all()



###############################################################################
# 						          USUARIOS                                    #
###############################################################################

usuario_1 = clsUsuario('aldrix', 'Aldrix Marfil', '1234.ABCD', 'aldrixmarfil@gmail.com', 4129343515)
usuario_2 = clsUsuario('ascander', 'Ascander Suarez', '1234.ABCD', 'ascander@gmail.com', 1111111111)
usuario_3 = clsUsuario('jcguzman', 'Jean Carlos Guzman', '1234.ABCD', 'jcguzman@gmail.com', 2222222222)

db.session.add(usuario_1)
db.session.add(usuario_2)
db.session.add(usuario_3)
db.session.commit()

usuarios = clsUsuario.query.all()

print('\nUsuarios registrados:')
for usuario in usuarios:
	print('\t' + str(usuario))
print('\n')



###############################################################################
#                                  DISENOS                                    #
###############################################################################

prop_diseno_1 = {'cant_casos_uso':30}
prop_diseno_2 = {'cant_casos_uso':20}

diseno_1 = clsDiseno('Diseno 1', 'Diseno para una aplicacion web de diagramas', json.dumps(prop_diseno_1))
diseno_2 = clsDiseno('Diseno 2', 'Diseno para una aplicacion web de juegos', json.dumps(prop_diseno_2))

db.session.add(diseno_1)
db.session.add(diseno_2)
db.session.commit()

disenos = clsDiseno.query.all()

print('Disenos almacenados:')
for diseno in disenos:
    print('\t' + str(diseno))
print('\n')



###############################################################################
#                      DISENOS ASOCIADOS A USUARIOS                           #
###############################################################################

# Obtenemos los usuarios por nombreUsuario.
usuario_1 = clsUsuario.query.filter_by(nombreUsuario='aldrix').first()
usuario_2 = clsUsuario.query.filter_by(nombreUsuario='ascander').first()
usuario_3 = clsUsuario.query.filter_by(nombreUsuario='jcguzman').first()

# Obtenemos los disenos por nombre.
diseno_1 = clsDiseno.query.filter_by(nombre='Diseno 1').first()
diseno_2 = clsDiseno.query.filter_by(nombre='Diseno 2').first()

asociacion_1 = clsDisenosAsociadosUsuario(diseno_1.idDiseno, usuario_1.idUsuario)
asociacion_2 = clsDisenosAsociadosUsuario(diseno_1.idDiseno, usuario_2.idUsuario)
asociacion_3 = clsDisenosAsociadosUsuario(diseno_2.idDiseno, usuario_3.idUsuario)

db.session.add(asociacion_1)
db.session.add(asociacion_2)
db.session.add(asociacion_3)
db.session.commit()

asociaciones = clsDisenosAsociadosUsuario.query.all()

print('Asociaciones entre disenos y usuarios resgistrados:')
for asociacion in asociaciones:
    print('\t' + str(asociacion))
print('\n')



###############################################################################
#                                 DIAGRAMAS                                   #
###############################################################################

prop_diagrama_1 = {'color_vistas': '#CCCCCC'}
prop_diagrama_2 = {'color_vistas': '#FFFFFF'}
prop_diagrama_3 = {'color_vistas': '#CCCCCC'}

diagrama_1 = clsDiagrama('Diagrama 1', 'Diagrama para el sistema de login', json.dumps(prop_diagrama_1), disenos[0].idDiseno)
diagrama_2 = clsDiagrama('Diagrama 2', 'Diagrama para la creacion de proyectos', json.dumps(prop_diagrama_2), disenos[0].idDiseno)
diagrama_3 = clsDiagrama('Diagrama 3', 'Diagrama para el registro de juegos', json.dumps(prop_diagrama_3), disenos[1].idDiseno)

db.session.add(diagrama_1)
db.session.add(diagrama_2)
db.session.add(diagrama_3)
db.session.commit()

diagramas = clsDiagrama.query.all()

print('Diagramas almacenados:')
i = 0
for diagrama in diagramas:
    print('\t' + str(diagrama) + ' asociado al diseno: ' + str(i + 1))
print('\n')



###############################################################################
#                                 ENTIDAD                                     #
###############################################################################

prop_nodo_vacio = {}

entidad_1 = clsEntidad('EConexion', json.dumps(prop_nodo_vacio), disenos[0].idDiseno)
entidad_2 = clsEntidad('EAcceso', json.dumps(prop_nodo_vacio), disenos[0].idDiseno)
entidad_3 = clsEntidad('EUsuario', json.dumps(prop_nodo_vacio), disenos[0].idDiseno)
entidad_4 = clsEntidad('EProyecto', json.dumps(prop_nodo_vacio), disenos[0].idDiseno)

db.session.add(entidad_1)
db.session.add(entidad_2)
db.session.add(entidad_3)
db.session.add(entidad_4)

db.session.commit()


entidades = clsEntidad.query.all()

print('Entidades almacenados asociadas al Diseno 1:')
for entidad in entidades:
    print('\t' + str(entidad))
print('\n')



###############################################################################
#                                   NODOS                                     #
###############################################################################

prop_nodo_vacio = {}

# ASOCIADOS AL DIAGRAMA 1.
prop_vista_1 = {'campos': ['usuario','clave'], 'botones': ['conectarse','registrarse']}
prop_vista_2 = {'campos': [], 'botones': ['desconectarse','crearProyecto']}
prop_vista_3 = {'campos': ['nombre','usuario','correo','telefono'], 'botones': ['registrarse']}

vista_1 = clsVista('VInicio', 'vista', json.dumps(prop_vista_1), diagramas[0].idDiagrama)
vista_2 = clsVista('VPrincipal', 'vista', json.dumps(prop_vista_2), diagramas[0].idDiagrama)
vista_3 = clsVista('VRegistro', 'vista', json.dumps(prop_vista_3), diagramas[0].idDiagrama)

accion_1 = clsAccion('AConectarse', 'accion', json.dumps(prop_nodo_vacio), diagramas[0].idDiagrama)
accion_2 = clsAccion('ADesconectarse', 'accion', json.dumps(prop_nodo_vacio), diagramas[0].idDiagrama)
accion_3 = clsAccion('ARegistrarse', 'accion', json.dumps(prop_nodo_vacio), diagramas[0].idDiagrama)

operacion_1 = clsOperacion('OConectarse', 'operacion', json.dumps(prop_nodo_vacio), diagramas[0].idDiagrama, entidades[0].idEntidad)
operacion_2 = clsOperacion('OVerificarClave', 'operacion', json.dumps(prop_nodo_vacio), diagramas[0].idDiagrama, entidades[1].idEntidad)
operacion_3 = clsOperacion('ORegistrarse', 'operacion', json.dumps(prop_nodo_vacio), diagramas[0].idDiagrama, entidades[2].idEntidad)
operacion_4 = clsOperacion('OVerificarUsuarioExiste', 'operacion', json.dumps(prop_nodo_vacio), diagramas[0].idDiagrama, entidades[2].idEntidad)
operacion_5 = clsOperacion('ODesconectarse', 'operacion', json.dumps(prop_nodo_vacio), diagramas[0].idDiagrama, None)
operacion_6 = clsOperacion('OOperacionX', 'operacion', json.dumps(prop_nodo_vacio), diagramas[0].idDiagrama, entidades[1].idEntidad)


# ASOCIADOS AL DIAGRAMA 2.
prop_vista_4 = {'campos': ['nombre', 'descripcion'], 'botones': ['crear']}
prop_vista_5 = {'campos': [], 'botones': ['desconectarse']}

vista_4 = clsVista('VCrearProyecto', 'vista', json.dumps(prop_vista_4), diagramas[1].idDiagrama)
vista_5 = clsVista('VProyecto', 'vista', json.dumps(prop_vista_5), diagramas[1].idDiagrama)

accion_4 = clsAccion('ACrearProyecto', 'accion', json.dumps(prop_nodo_vacio), diagramas[1].idDiagrama)

operacion_7 = clsOperacion('OListarProyectos', 'operacion', json.dumps(prop_nodo_vacio), diagramas[1].idDiagrama, entidades[3].idEntidad)
operacion_8 = clsOperacion('OVerificarProyectoExiste', 'operacion', json.dumps(prop_nodo_vacio), diagramas[1].idDiagrama, entidades[3].idEntidad)

db.session.add(vista_1)
db.session.add(vista_2)
db.session.add(vista_3)
db.session.add(vista_4)
db.session.add(vista_5)

db.session.add(accion_1)
db.session.add(accion_2)
db.session.add(accion_3)
db.session.add(accion_4)

db.session.add(operacion_1)
db.session.add(operacion_2)
db.session.add(operacion_3)
db.session.add(operacion_4)
db.session.add(operacion_5)
db.session.add(operacion_6)
db.session.add(operacion_7)
db.session.add(operacion_8)

db.session.commit()


# NODOS EXTERNOS ASOCIADOS AL DIAGRAMA 1.
nodo      = clsNodo.query.filter_by(nombre='VProyecto').first()
externo_1 = clsExterno('VProyecto', 'externo', json.dumps(prop_nodo_vacio), diagramas[0].idDiagrama, nodo.idNodo)

nodo      = clsNodo.query.filter_by(nombre='ACrearProyecto').first()
externo_2 = clsExterno('ACrearProyecto', 'externo', json.dumps(prop_nodo_vacio), diagramas[0].idDiagrama, nodo.idNodo)


# NODOS EXTERNOS ASOCIADOS AL DIAGRAMA 2.
nodo      = clsNodo.query.filter_by(nombre='VPrincipal').first()
externo_3 = clsExterno('VPrincipal', 'externo', json.dumps(prop_nodo_vacio), diagramas[1].idDiagrama, nodo.idNodo)

nodo      = clsNodo.query.filter_by(nombre='ADesconectarse').first() 
externo_4 = clsExterno('ADesconectarse', 'externo', json.dumps(prop_nodo_vacio), diagramas[1].idDiagrama, nodo.idNodo)


db.session.add(externo_1)
db.session.add(externo_2)
db.session.add(externo_3)
db.session.add(externo_4)

db.session.commit()


nodos = db.session.query(clsNodo).all()

print('Nodos almacenados asociados al Diagrama 1:')
for nodo in nodos:
    print('\t' + str(nodo))
print('\n')



###############################################################################
#                                 RELACION                                    #
###############################################################################

prop_relacion_vacio = {}

relacion_va_1  = clsRelacion('ok', 'vista-accion', json.dumps(prop_relacion_vacio), nodos[7].idNodo, nodos[0].idNodo, diagramas[0].idDiagrama)
relacion_va_2  = clsRelacion('error', 'vista-accion', json.dumps(prop_relacion_vacio), nodos[7].idNodo, nodos[2].idNodo, diagramas[0].idDiagrama)
relacion_va_3  = clsRelacion(None, 'vista-accion', json.dumps(prop_relacion_vacio), nodos[2].idNodo, nodos[7].idNodo, diagramas[0].idDiagrama)
relacion_va_4  = clsRelacion(None, 'vista-accion', json.dumps(prop_relacion_vacio), nodos[0].idNodo, nodos[5].idNodo, diagramas[0].idDiagrama)
relacion_va_5  = clsRelacion('error', 'vista-accion', json.dumps(prop_relacion_vacio), nodos[5].idNodo, nodos[0].idNodo, diagramas[0].idDiagrama)
relacion_va_6  = clsRelacion('ok', 'vista-accion', json.dumps(prop_relacion_vacio), nodos[5].idNodo, nodos[1].idNodo, diagramas[0].idDiagrama)
relacion_va_7  = clsRelacion(None, 'vista-accion', json.dumps(prop_relacion_vacio), nodos[1].idNodo, nodos[6].idNodo, diagramas[0].idDiagrama)
relacion_va_8  = clsRelacion('error', 'vista-accion', json.dumps(prop_relacion_vacio), nodos[6].idNodo, nodos[0].idNodo, diagramas[0].idDiagrama)

relacion_ao_1  = clsRelacion(None, 'accion-operacion', json.dumps(prop_relacion_vacio), nodos[7].idNodo, nodos[11].idNodo, diagramas[0].idDiagrama)
relacion_ao_2  = clsRelacion(None, 'accion-operacion', json.dumps(prop_relacion_vacio), nodos[7].idNodo, nodos[12].idNodo, diagramas[0].idDiagrama)
relacion_ao_3  = clsRelacion(None, 'accion-operacion', json.dumps(prop_relacion_vacio), nodos[5].idNodo, nodos[10].idNodo, diagramas[0].idDiagrama)
relacion_ao_4  = clsRelacion(None, 'accion-operacion', json.dumps(prop_relacion_vacio), nodos[5].idNodo, nodos[9].idNodo, diagramas[0].idDiagrama)
relacion_ao_5  = clsRelacion(None, 'accion-operacion', json.dumps(prop_relacion_vacio), nodos[6].idNodo, nodos[13].idNodo, diagramas[0].idDiagrama)

relacion_vo_1  = clsRelacion(None, 'vista-operacion', json.dumps(prop_relacion_vacio), nodos[2].idNodo, nodos[14].idNodo, diagramas[0].idDiagrama)

relacion_ev_1  = clsRelacion(None, 'externo-vista', json.dumps(prop_relacion_vacio), nodos[1].idNodo, nodos[18].idNodo, diagramas[0].idDiagrama)

relacion_ea_1  = clsRelacion(None, 'externo-accion', json.dumps(prop_relacion_vacio), nodos[17].idNodo, nodos[6].idNodo, diagramas[0].idDiagrama)



relacion_va_9  = clsRelacion('error', 'vista-accion', json.dumps(prop_relacion_vacio), nodos[8].idNodo, nodos[3].idNodo, diagramas[1].idDiagrama)
relacion_va_10 = clsRelacion('ok', 'vista-accion', json.dumps(prop_relacion_vacio), nodos[8].idNodo, nodos[4].idNodo, diagramas[1].idDiagrama)
relacion_va_11 = clsRelacion(None, 'vista-accion', json.dumps(prop_relacion_vacio), nodos[3].idNodo, nodos[8].idNodo, diagramas[1].idDiagrama)

relacion_ao_6  = clsRelacion(None, 'accion-operacion', json.dumps(prop_relacion_vacio), nodos[8].idNodo, nodos[16].idNodo, diagramas[1].idDiagrama)

relacion_vo_2  = clsRelacion(None, 'vista-operacion', json.dumps(prop_relacion_vacio), nodos[17].idNodo, nodos[15].idNodo, diagramas[1].idDiagrama)

relacion_ev_2  = clsRelacion(None, 'externo-vista', json.dumps(prop_relacion_vacio), nodos[4].idNodo, nodos[20].idNodo, diagramas[1].idDiagrama)

relacion_ea_2  = clsRelacion(None, 'externo-accion', json.dumps(prop_relacion_vacio), nodos[19].idNodo, nodos[8].idNodo, diagramas[1].idDiagrama)

db.session.add(relacion_va_1)
db.session.add(relacion_va_2)
db.session.add(relacion_va_3)
db.session.add(relacion_va_4)
db.session.add(relacion_va_5)
db.session.add(relacion_va_6)
db.session.add(relacion_va_7)
db.session.add(relacion_va_8)
db.session.add(relacion_va_9)
db.session.add(relacion_va_10)
db.session.add(relacion_va_11)

db.session.add(relacion_ao_1)
db.session.add(relacion_ao_2)
db.session.add(relacion_ao_3)
db.session.add(relacion_ao_4)
db.session.add(relacion_ao_5)
db.session.add(relacion_ao_6)

db.session.add(relacion_vo_1)
db.session.add(relacion_vo_2)

db.session.add(relacion_ev_1)
db.session.add(relacion_ev_2)

db.session.add(relacion_ea_1)
db.session.add(relacion_ea_2)

db.session.commit()

relaciones = clsRelacion.query.all()

print('Relaciones almacenadas:')
for rela in relaciones:
    print('\t' + str(rela))
print('\n')

db.session.remove()
db.drop_all()
app_context.pop()