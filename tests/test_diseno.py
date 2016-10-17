# -*- coding: utf-8 -*-.

# DESCRIPCION: Pruebas unitarias para verificar la funcionalidad de la clase 
#              Diseno.


# Se importan las librerias necesarias.
import sys
import unittest

from flask import current_app
from app   import create_app, db

# Permite importar el modulo claseDiseno.
sys.path.append('./app/model')
from claseDiseno import *



# Declaracion de constantes.
TAM_MAX_NOMBRE = 64


class PruebaClaseDiseno(unittest.TestCase):

    def setUp(self):
        '''Datos necesarios al inicio'''

        self.app = create_app('pruebas')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.nombre      = 'Diseno '
        self.descripcion = 'Diseno para una aplicacion web'
        self.propiedades = {'prop1':'valor1', 'prop2':'valor2'}


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()



    #############################################
    #          Pruebas para crearDiseno         #
    #############################################

    def testCrearDisenoValido(self):
        oDiseno   = Diseno() 
        resultado = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        self.assertTrue(resultado)


    def testCrearDisenoRepetido(self):
        oDiseno    = Diseno()
        resultado1 = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        resultado2 = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        self.assertTrue(resultado2)


    def testCrearDisenoNombreTamanoCero(self):
        oDiseno   = Diseno() 
        resultado = oDiseno.crearDiseno('', self.descripcion, json.dumps(self.propiedades))
        self.assertTrue(resultado)


    def testCrearDisenoNombreTamanoMaximo(self):
        oDiseno   = Diseno() 
        resultado = oDiseno.crearDiseno('X'*TAM_MAX_NOMBRE, self.descripcion, json.dumps(self.propiedades))
        self.assertTrue(resultado)


    def testCrearDisenoNombreTamanoMayorAlMaximo(self):
        oDiseno   = Diseno() 
        resultado = oDiseno.crearDiseno('X'*(TAM_MAX_NOMBRE + 1), self.descripcion, json.dumps(self.propiedades))
        self.assertFalse(resultado)


    def testCrearDisenoNombreNone(self):
        oDiseno   = Diseno() 
        resultado = oDiseno.crearDiseno(None, self.descripcion, json.dumps(self.propiedades))
        self.assertFalse(resultado)


    def testCrearDisenoDescripcionTamCero(self):
        oDiseno   = Diseno() 
        resultado = oDiseno.crearDiseno(self.nombre, '', json.dumps(self.propiedades))
        self.assertTrue(resultado)


    def testCrearDisenoDescripcionNone(self):
        oDiseno   = Diseno() 
        resultado = oDiseno.crearDiseno(self.nombre, None, json.dumps(self.propiedades))
        self.assertFalse(resultado)


    def testCrearDisenoPropiedadesVacio(self):
        oDiseno   = Diseno() 
        resultado = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps({}))
        self.assertTrue(resultado)


    def testCrearDisenoPropiedadesNone(self):
        oDiseno   = Diseno() 
        resultado = oDiseno.crearDiseno(self.nombre, self.descripcion, None)
        self.assertFalse(resultado)


    def testCrearDisenoNombreTamCeroDescripcionTamCero(self):
        oDiseno   = Diseno() 
        resultado = oDiseno.crearDiseno('', '', json.dumps(self.propiedades))
        self.assertTrue(resultado)


    def testCrearDisenoNombreTamCeroDescripcionTamCeroPropiedadesNone(self):
        oDiseno   = Diseno() 
        resultado = oDiseno.crearDiseno('', '', None)
        self.assertFalse(resultado)


    def testCrearDisenoNombreNoneDescripcionNonePropiedadesNone(self):
        oDiseno   = Diseno() 
        resultado = oDiseno.crearDiseno(None, None, None)
        self.assertFalse(resultado)



    #############################################
    #         Pruebas para obtenerDisenos       #
    #############################################

    def testObtenerDisenosResultadoTamano1(self):
        oDiseno    = Diseno()
        resultado1 = oDiseno.crearDiseno(self.nombre+str(1), self.descripcion, json.dumps(self.propiedades))
       
        disenos = oDiseno.obtenerDisenos()
        self.assertEqual(len(disenos),1)


    def testObtenerDisenosResultadoTamano3(self):
        oDiseno    = Diseno()
        resultado1 = oDiseno.crearDiseno(self.nombre+str(1), self.descripcion, json.dumps(self.propiedades))
        resultado2 = oDiseno.crearDiseno(self.nombre+str(2), self.descripcion, json.dumps(self.propiedades))
        resultado3 = oDiseno.crearDiseno(self.nombre+str(3), self.descripcion, json.dumps(self.propiedades))
		
        disenos = oDiseno.obtenerDisenos()
        self.assertEqual(len(disenos),3)



    #############################################
    #         Pruebas para existeDiseno         #
    #############################################

    def testExisteDisenoValido(self):
        oDiseno    = Diseno()
        resultado1 = oDiseno.crearDiseno(self.nombre+str(4), self.descripcion, json.dumps(self.propiedades))
        diseno     = oDiseno.obtenerDisenosPorNombreYDescripcion(self.nombre+str(4), self.descripcion)
        idDiseno   = diseno[0].idDiseno

        existe = oDiseno.existeDiseno(idDiseno)
        self.assertTrue(existe)


    def testExisteDisenoNegativo(self):
        oDiseno = Diseno()
        existe  = oDiseno.existeDiseno(-1)
        self.assertFalse(existe)


    def testExisteDisenoCero(self):
        oDiseno = Diseno()
        existe  = oDiseno.existeDiseno(0)
        self.assertFalse(existe)


    def testExisteDisenoNone(self):
        oDiseno = Diseno()
        existe  = oDiseno.existeDiseno(None)
        self.assertFalse(existe)



    #############################################
    #     Pruebas para obtenerDisenoPorID       #
    #############################################

    def testObtenerDisenoPorIDValido(self):
        oDiseno    = Diseno()
        resultado1 = oDiseno.crearDiseno(self.nombre+str(5), self.descripcion, json.dumps(self.propiedades))
        diseno     = oDiseno.obtenerDisenosPorNombreYDescripcion(self.nombre+str(5), self.descripcion)
        idDiseno   = diseno[0].idDiseno

        existe = oDiseno.obtenerDisenoPorID(idDiseno)
        self.assertTrue(existe)


    def testObtenerDisenoPorIDNegativo(self):
        oDiseno = Diseno()
        existe  = oDiseno.obtenerDisenoPorID(-1)
        self.assertFalse(existe)


    def testObtenerDisenoPorIDCero(self):
        oDiseno = Diseno()
        existe  = oDiseno.obtenerDisenoPorID(0)
        self.assertFalse(existe)
        

    def testObtenerDisenoPorIDNone(self):
        oDiseno = Diseno()
        existe  = oDiseno.obtenerDisenoPorID(None)
        self.assertFalse(existe)



    #############################################
    #   Pruebas para obtenerDisenosPorNombre    #
    #############################################

    def testObtenerDisenosValidoResultadoTamano1(self):
        oDiseno = Diseno() 
        creado  = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        disenos = oDiseno.obtenerDisenosPorNombre(self.nombre)
        self.assertEqual(len(disenos), 1)


    def testObtenerDisenosValidoResultadoTamano2(self):
        oDiseno = Diseno() 
        creado1 = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        creado1 = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        disenos = oDiseno.obtenerDisenosPorNombre(self.nombre)
        self.assertEqual(len(disenos), 2)


    def testObtenerDisenosPorNombreTamanoCero(self):
        oDiseno = Diseno() 
        creado  = oDiseno.crearDiseno('', self.descripcion, json.dumps(self.propiedades))
        disenos = oDiseno.obtenerDisenosPorNombre('')
        self.assertEqual(len(disenos), 1)


    def testObtenerDisenosPorNombreTamanoMaximo(self):
        oDiseno = Diseno() 
        creado  = oDiseno.crearDiseno('X'*TAM_MAX_NOMBRE, self.descripcion, json.dumps(self.propiedades))
        disenos = oDiseno.obtenerDisenosPorNombre('X'*TAM_MAX_NOMBRE)
        self.assertEqual(len(disenos), 1)


    def testObtenerDisenosPorNombreTamanoMayorAlMaximo(self):
        oDiseno = Diseno() 
        creado  = oDiseno.crearDiseno('X'*(TAM_MAX_NOMBRE+1), self.descripcion, json.dumps(self.propiedades))
        disenos = oDiseno.obtenerDisenosPorNombre('X'*(TAM_MAX_NOMBRE+1))
        self.assertEqual(len(disenos), 0)


    def testObtenerDisenosPorNombreNone(self):
        oDiseno = Diseno() 
        disenos = oDiseno.obtenerDisenosPorNombre(None)
        self.assertEqual(len(disenos), 0)


    
    ####################################################
    # Pruebas para obtenerDisenosPorNombreYDescripcion #
    ####################################################


    def testObtenerDisenosPorNombreYDescripcionValidoResultadoTamano1(self):
        oDiseno = Diseno()
        creado  = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        disenos = oDiseno.obtenerDisenosPorNombreYDescripcion(self.nombre, self.descripcion)
        self.assertEqual(len(disenos), 1)


    def testObtenerDisenosPorNombreYDescripcionValidoResultadoTamano2(self):
        oDiseno = Diseno()
        creado1 = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        creado2 = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        disenos = oDiseno.obtenerDisenosPorNombreYDescripcion(self.nombre, self.descripcion)
        self.assertEqual(len(disenos), 2)


    def testObtenerDisenosPorNombreYDescripcionNombreTamCero(self):
        oDiseno = Diseno()
        creado  = oDiseno.crearDiseno('', self.descripcion, json.dumps(self.propiedades))
        disenos = oDiseno.obtenerDisenosPorNombreYDescripcion('', self.descripcion)
        self.assertEqual(len(disenos), 1)


    def testObtenerDisenosPorNombreYDescripcionNombreTamMaximo(self):
        oDiseno = Diseno()
        creado  = oDiseno.crearDiseno('X'*TAM_MAX_NOMBRE, self.descripcion, json.dumps(self.propiedades))
        disenos = oDiseno.obtenerDisenosPorNombreYDescripcion('X'*TAM_MAX_NOMBRE, self.descripcion)
        self.assertEqual(len(disenos), 1)


    def testObtenerDisenosPorNombreYDescripcionNombreMayorAlMaximo(self):
        oDiseno = Diseno()
        creado  = oDiseno.crearDiseno('X'*(TAM_MAX_NOMBRE+1), self.descripcion, json.dumps(self.propiedades))
        disenos = oDiseno.obtenerDisenosPorNombreYDescripcion('X'*(TAM_MAX_NOMBRE+1), self.descripcion)
        self.assertEqual(len(disenos), 0)


    def testObtenerDisenosPorNombreYDescripcionNombreNone(self):
        oDiseno = Diseno()
        disenos = oDiseno.obtenerDisenosPorNombreYDescripcion(None, self.descripcion)
        self.assertEqual(len(disenos), 0)


    def testObtenerDisenosPorNombreYDescripcionDescripcionTamCero(self):
        oDiseno = Diseno()
        creado  = oDiseno.crearDiseno(self.nombre, '', json.dumps(self.propiedades))
        disenos = oDiseno.obtenerDisenosPorNombreYDescripcion(self.nombre, '')
        self.assertEqual(len(disenos), 1)

    def testObtenerDisenosPorNombreYDescripcionDescripcionNone(self):
        oDiseno = Diseno()
        disenos = oDiseno.obtenerDisenosPorNombreYDescripcion(self.nombre, None)
        self.assertEqual(len(disenos), 0)


    def testObtenerDisenosPorNombreYDescripcionNombreTamCeroDescTamanoCero(self):
        oDiseno = Diseno()
        creado  = oDiseno.crearDiseno('', '', json.dumps(self.propiedades))
        disenos = oDiseno.obtenerDisenosPorNombreYDescripcion('', '')
        self.assertEqual(len(disenos), 1)

    def testObtenerDisenosPorNombreYDescripcionNombreNoneDescripcionNone(self):
        oDiseno = Diseno()
        disenos = oDiseno.obtenerDisenosPorNombreYDescripcion(None, None)
        self.assertEqual(len(disenos), 0)



    #############################################
    #       Pruebas para actualizarDiseno       #
    #############################################

    def testActualizarDisenoValido(self):
        oDiseno     = Diseno()
        creado      = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        diseno      = oDiseno.obtenerDisenosPorNombre(self.nombre)
        idDiseno    = diseno[0].idDiseno
        actualizado = oDiseno.actualizarDiseno(idDiseno, self.nombre+str(1), self.descripcion+str(1), json.dumps({'prop3': 'valor3'}))
        self.assertTrue(actualizado)


    def testActualizarDisenoRepetido(self):
        oDiseno     = Diseno()
        creado      = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        diseno      = oDiseno.obtenerDisenosPorNombre(self.nombre)
        idDiseno    = diseno[0].idDiseno
        actualizado = oDiseno.actualizarDiseno(idDiseno, self.nombre+str(1), self.descripcion+str(1), json.dumps({'prop3': 'valor3'}))
        actualizado = oDiseno.actualizarDiseno(idDiseno, self.nombre+str(1), self.descripcion+str(1), json.dumps({'prop3': 'valor3'}))
        self.assertTrue(actualizado)


    def testActualizarDisenoIDCero(self):
        oDiseno     = Diseno()
        actualizado = oDiseno.actualizarDiseno(0, self.nombre+str(1), self.descripcion+str(1), json.dumps({'prop3': 'valor3'}))
        self.assertFalse(actualizado)


    def testActualizarDisenoIDNegativo(self):
        oDiseno     = Diseno()
        actualizado = oDiseno.actualizarDiseno(-1, self.nombre+str(1), self.descripcion+str(1), json.dumps({'prop3': 'valor3'}))
        self.assertFalse(actualizado)


    def testActualizarDisenoIDNone(self):
        oDiseno     = Diseno()
        actualizado = oDiseno.actualizarDiseno(None, self.nombre+str(1), self.descripcion+str(1), json.dumps({'prop3': 'valor3'}))
        self.assertFalse(actualizado)


    def testActualizarDisenoNombreTamanoCero(self):
        oDiseno     = Diseno()
        creado      = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        diseno      = oDiseno.obtenerDisenosPorNombre(self.nombre)
        idDiseno    = diseno[0].idDiseno
        actualizado = oDiseno.actualizarDiseno(idDiseno, '', self.descripcion+str(1), json.dumps({'prop3': 'valor3'}))
        self.assertTrue(actualizado)


    def testActualizarDisenoNombreTamanoMaximo(self):
        oDiseno     = Diseno()
        creado      = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        diseno      = oDiseno.obtenerDisenosPorNombre(self.nombre)
        idDiseno    = diseno[0].idDiseno
        actualizado = oDiseno.actualizarDiseno(idDiseno, 'X'*TAM_MAX_NOMBRE, self.descripcion+str(1), json.dumps({'prop3': 'valor3'}))
        self.assertTrue(actualizado)


    def testActualizarDisenoNombreTamanoMayorAlMaximo(self):
        oDiseno     = Diseno()
        creado      = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        diseno      = oDiseno.obtenerDisenosPorNombre(self.nombre)
        idDiseno    = diseno[0].idDiseno
        actualizado = oDiseno.actualizarDiseno(idDiseno, 'X'*(TAM_MAX_NOMBRE+1), self.descripcion+str(1), json.dumps({'prop3': 'valor3'}))
        self.assertFalse(actualizado)


    def testActualizarDisenoNombreNone(self):
        oDiseno     = Diseno()
        creado      = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        diseno      = oDiseno.obtenerDisenosPorNombre(self.nombre)
        idDiseno    = diseno[0].idDiseno
        actualizado = oDiseno.actualizarDiseno(idDiseno, None, self.descripcion+str(1), json.dumps({'prop3': 'valor3'}))
        self.assertFalse(actualizado)


    def testActualizarDisenoDescripcionTamanoCero(self):
        oDiseno     = Diseno()
        creado      = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        diseno      = oDiseno.obtenerDisenosPorNombre(self.nombre)
        idDiseno    = diseno[0].idDiseno
        actualizado = oDiseno.actualizarDiseno(idDiseno, self.nombre+str(1), '', json.dumps({'prop3': 'valor3'}))
        self.assertTrue(actualizado)


    def testActualizarDisenoDescripcionNone(self):
        oDiseno     = Diseno()
        creado      = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        diseno      = oDiseno.obtenerDisenosPorNombre(self.nombre)
        idDiseno    = diseno[0].idDiseno
        actualizado = oDiseno.actualizarDiseno(idDiseno, self.nombre+str(1), None, json.dumps({'prop3': 'valor3'}))
        self.assertFalse(actualizado)


    def testActualizarDisenoPropiedadesVacia(self):
        oDiseno     = Diseno()
        creado      = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        diseno      = oDiseno.obtenerDisenosPorNombre(self.nombre)
        idDiseno    = diseno[0].idDiseno
        actualizado = oDiseno.actualizarDiseno(idDiseno, self.nombre+str(1), self.descripcion+str(1), json.dumps({}))
        self.assertTrue(actualizado)


    def testActualizarDisenoPropiedadesNone(self):
        oDiseno     = Diseno()
        creado      = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        diseno      = oDiseno.obtenerDisenosPorNombre(self.nombre)
        idDiseno    = diseno[0].idDiseno
        actualizado = oDiseno.actualizarDiseno(idDiseno, self.nombre+str(1), self.descripcion+str(1), None)
        self.assertFalse(actualizado)


    def testActualizarDisenoIDCeroNombreNone(self):
        oDiseno     = Diseno()
        actualizado = oDiseno.actualizarDiseno(0, None, self.descripcion, json.dumps({'prop3': 'valor3'}))
        self.assertFalse(actualizado)


    def testActualizarDisenoIDCeroDescripcionNone(self):
        oDiseno     = Diseno()
        actualizado = oDiseno.actualizarDiseno(0, self.nombre, None, json.dumps({'prop3': 'valor3'}))
        self.assertFalse(actualizado)


    def testActualizarDisenoIDCeroPropiedadesNone(self):
        oDiseno     = Diseno()
        actualizado = oDiseno.actualizarDiseno(0, self.nombre, self.descripcion, None)
        self.assertFalse(actualizado)


    def testActualizarDisenoIDNoneNombreNone(self):
        oDiseno     = Diseno()
        actualizado = oDiseno.actualizarDiseno(None, None, self.descripcion, json.dumps({'prop3': 'valor3'}))
        self.assertFalse(actualizado)


    def testActualizarDisenoIDNoneDescripcionNone(self):
        oDiseno     = Diseno()
        actualizado = oDiseno.actualizarDiseno(None, self.nombre, None, json.dumps({'prop3': 'valor3'}))
        self.assertFalse(actualizado)


    def testActualizarDisenoIDNonePropiedadesNone(self):
        oDiseno     = Diseno()
        actualizado = oDiseno.actualizarDiseno(None, self.nombre, self.descripcion, None)
        self.assertFalse(actualizado)


    def testActualizarDisenoNombreNoneDescripcionNone(self):
        oDiseno     = Diseno()
        creado      = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        diseno      = oDiseno.obtenerDisenosPorNombre(self.nombre)
        idDiseno    = diseno[0].idDiseno
        actualizado = oDiseno.actualizarDiseno(idDiseno, None, None, json.dumps({'prop3': 'valor3'}))
        self.assertFalse(actualizado)


    def testActualizarDisenoIDNoneNombreNoneDescripcionNonePropiedadesNone(self):
        oDiseno     = Diseno()
        actualizado = oDiseno.actualizarDiseno(None, None, None, None)
        self.assertFalse(actualizado)



    #############################################
    #        Pruebas para eliminarDiseno        #
    #############################################

    def testEliminarDisenoValido(self):
        oDiseno   = Diseno()
        creado    = oDiseno.crearDiseno(self.nombre, self.descripcion, json.dumps(self.propiedades))
        diseno    = oDiseno.obtenerDisenosPorNombre(self.nombre)
        idDiseno  = diseno[0].idDiseno
        eliminado = oDiseno.eliminarDiseno(idDiseno)
        self.assertTrue(eliminado)


    def testEliminarDisenoIDCero(self):
        oDiseno   = Diseno()
        eliminado = oDiseno.eliminarDiseno(0)
        self.assertFalse(eliminado)


    def testEliminarDisenoIDNegativo(self):
        oDiseno   = Diseno()
        eliminado = oDiseno.eliminarDiseno(-1)
        self.assertFalse(eliminado)


    def testEliminarDisenoIDNone(self):
        oDiseno   = Diseno()
        eliminado = oDiseno.eliminarDiseno(None)
        self.assertFalse(eliminado)