# -*- coding: utf-8 -*-.

# DESCRIPCION: Pruebas unitarias para verificar la funcionalidad de la clase 
#              Nodo.


# Se importan las librerias necesarias.
import sys
import unittest

from flask import current_app, json
from app   import create_app, db

# Permite importar el modulo claseNodo.
sys.path.append('./app/model')
from claseNodo import *


# Declaracion de constantes.
TAM_MAX_NOMBRE = 60


class PruebaClaseNodo(unittest.TestCase):

    def setUp(self):
        '''Datos necesarios al inicio'''

        self.app = create_app('pruebas')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.nombre      = 'Nodo '
        self.tipo        = 'nodo'
        self.propiedades = {'prop1':'valor1', 'prop2':'valor2'}

        #Creamos un diseno.
        nuevoDiseno = clsDiseno('Diseno', 'Diseno para una aplicacion web', 1,json.dumps(self.propiedades))
        db.session.add(nuevoDiseno)
        db.session.commit()
        diseno        = clsDiseno.query.filter_by(nombre='Diseno').first()
        self.idDiseno = diseno.idDiseno

        #Creamos un diagrama 1.
        nuevoDiagrama = clsDiagrama('Diagrama1', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama         = clsDiagrama.query.filter_by(nombre='Diagrama1').first()
        self.idDiagrama = diagrama.idDiagrama


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()



    # #############################################
    # #          Pruebas para crearNodo           #
    # #############################################

    # def testCrearNodoValido(self):
    #     oNodo     = Nodo()
    #     resultado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     self.assertTrue(True)


    # def testCrearNodoRepetido(self):
    #     oNodo      = Nodo()
    #     resultado1 = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     resultado2 = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     self.assertTrue(resultado2)


    # def testCrearNodoTipoVista(self):
    #     oNodo     = Nodo()
    #     resultado = oNodo.crearNodo(self.nombre, 'vista', json.dumps(self.propiedades), self.idDiagrama)
    #     self.assertTrue(resultado)


    # def testCrearNodoTipoAccion(self):
    #     oNodo     = Nodo()
    #     resultado = oNodo.crearNodo(self.nombre, 'accion', json.dumps(self.propiedades), self.idDiagrama)
    #     self.assertTrue(resultado)


    # def testCrearNodoTipoOperacion(self):
    #     oNodo     = Nodo()
    #     resultado = oNodo.crearNodo(self.nombre, 'operacion', json.dumps(self.propiedades), self.idDiagrama)
    #     self.assertTrue(resultado)


    # def testCrearNodoTipoNone(self):
    #     oNodo     = Nodo()
    #     resultado = oNodo.crearNodo(self.nombre, None, json.dumps(self.propiedades), self.idDiagrama)
    #     self.assertFalse(resultado)


    # def testCrearNodoNombreTamanoCero(self):
    #     oNodo     = Nodo() 
    #     resultado = oNodo.crearNodo('', self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     self.assertTrue(resultado)


    # def testCrearNodoNombreTamanoMaximo(self):
    #     oNodo     = Nodo() 
    #     resultado = oNodo.crearNodo('X'*TAM_MAX_NOMBRE, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     self.assertTrue(resultado)


    # def testCrearNodoNombreTamanoMayorAlMaximo(self):
    #     oNodo     = Nodo() 
    #     resultado = oNodo.crearNodo('X'*(TAM_MAX_NOMBRE + 1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     self.assertFalse(resultado)


    # def testCrearNodoNombreNone(self):
    #     oNodo     = Nodo() 
    #     resultado = oNodo.crearNodo(None, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     self.assertFalse(resultado)


    # def testCrearNodoPropiedadesVacio(self):
    #     oNodo     = Nodo() 
    #     resultado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps({}),  self.idDiagrama)
    #     self.assertTrue(resultado)


    # def testCrearNodoPropiedadesNone(self):
    #     oNodo     = Nodo() 
    #     resultado = oNodo.crearNodo(self.nombre, self.tipo, None, self.idDiagrama)
    #     self.assertFalse(resultado)


    # def testCrearNodoIdDiagrama0(self):
    #     oNodo     = Nodo() 
    #     resultado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), 0)
    #     self.assertFalse(resultado)


    # def testCrearNodoIdDiagramaNegativo(self):
    #     oNodo     = Nodo() 
    #     resultado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), -1)
    #     self.assertFalse(resultado)


    # def testCrearNodoIdDiagramaNone(self):
    #     oNodo     = Nodo() 
    #     resultado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), None)
    #     self.assertFalse(resultado)


    # def testCrearNodoNombreNonePropiedadesNone(self):
    #     oNodo   = Nodo() 
    #     resultado = oNodo.crearNodo(None, self.tipo, None, self.idDiagrama)
    #     self.assertFalse(resultado)


    # def testCrearNodoNombreNoneIdDiagramaNone(self):
    #     oNodo   = Nodo() 
    #     resultado = oNodo.crearNodo(None, self.tipo,json.dumps(self.propiedades), None)
    #     self.assertFalse(resultado)


    # def testCrearNodoNombreNonePropiedadesNone(self):
    #     oNodo   = Nodo() 
    #     resultado = oNodo.crearNodo(None, self.tipo, None, self.idDiagrama)
    #     self.assertFalse(resultado)


    # def testCrearNodoArgumentosNone(self):
    #     oNodo   = Nodo() 
    #     resultado = oNodo.crearNodo(None, None, None, None)
    #     self.assertFalse(resultado)



    #############################################
    #       Pruebas para crearNodoExterno       #
    #############################################

    def testCrearNodoExternoValido(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado2 = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        self.assertTrue(True)


    def testCrearNodoExternoRepetido(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado2 = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        resultado3 = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        self.assertTrue(resultado3)


    def testCrearNodoExternoNombreTamanoCero(self):
        oNodo      = Nodo() 
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado  = oNodo.crearNodoExterno('', json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        self.assertTrue(resultado)


    def testCrearNodoExternoNombreTamanoMaximo(self):
        oNodo      = Nodo() 
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado  = oNodo.crearNodoExterno('X'*TAM_MAX_NOMBRE, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        self.assertTrue(resultado)


    def testCrearNodoExternoNombreTamanoMayorAlMaximo(self):
        oNodo      = Nodo() 
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado  = oNodo.crearNodoExterno('X'*(TAM_MAX_NOMBRE + 1), json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        self.assertFalse(resultado)


    def testCrearNodoExternoNombreNone(self):
        oNodo      = Nodo() 
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado  = oNodo.crearNodoExterno(None, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        self.assertFalse(resultado)


    def testCrearNodoExternoPropiedadesVacio(self):
        oNodo      = Nodo() 
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado  = oNodo.crearNodoExterno(self.nombre, json.dumps({}),  self.idDiagrama, idNodoExt)
        self.assertTrue(resultado)


    def testCrearNodoExternoPropiedadesNone(self):
        oNodo      = Nodo() 
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado  = oNodo.crearNodoExterno(self.nombre, None, self.idDiagrama, idNodoExt)
        self.assertFalse(resultado)


    def testCrearNodoExternoIdDiagrama0(self):
        oNodo      = Nodo() 
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado  = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), 0, idNodoExt)
        self.assertFalse(resultado)


    def testCrearNodoExternoIdDiagramaNegativo(self):
        oNodo      = Nodo() 
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado  = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), -1, idNodoExt)
        self.assertFalse(resultado)


    def testCrearNodoExternoIdDiagramaNone(self):
        oNodo      = Nodo() 
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado  = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), None, idNodoExt)
        self.assertFalse(resultado)


    def testCrearNodoExternoIdNodoExt0(self):
        oNodo      = Nodo() 
        resultado  = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, 0)
        self.assertFalse(resultado)


    def testCrearNodoExternoIdNodoExtNegativo(self):
        oNodo     = Nodo() 
        resultado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, -1)
        self.assertFalse(resultado)


    def testCrearNodoExternoIdNodoExtNone(self):
        oNodo     = Nodo() 
        resultado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, None)
        self.assertFalse(resultado)


    def testCrearNodoExternoNombreNonePropiedadesNone(self):
        oNodo      = Nodo() 
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado  = oNodo.crearNodoExterno(None, None, self.idDiagrama, idNodoExt)
        self.assertFalse(resultado)


    def testCrearNodoExternoNombreNoneIdDiagramaNone(self):
        oNodo      = Nodo() 
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado  = oNodo.crearNodoExterno(None, json.dumps(self.propiedades), None, idNodoExt)
        self.assertFalse(resultado)


    def testCrearNodoExternoNombreNoneIdNodoExtNone(self):
        oNodo     = Nodo() 
        resultado = oNodo.crearNodoExterno(None, json.dumps(self.propiedades), self.idDiagrama, None)
        self.assertFalse(resultado)


    def testCrearNodoExternoPropiedadesNoneIdNodoExtNegativo(self):
        oNodo     = Nodo() 
        resultado = oNodo.crearNodoExterno(self.nombre, None, self.idDiagrama, -1)
        self.assertFalse(resultado)


    def testCrearNodoExternoNombreNonePropiedadesNone(self):
        oNodo      = Nodo() 
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado  = oNodo.crearNodoExterno(None, None, self.idDiagrama, idNodoExt)
        self.assertFalse(resultado)


    def testCrearNodoExternoArgumentosNone(self):
        oNodo     = Nodo() 
        resultado = oNodo.crearNodoExterno(None, None, None, None)
        self.assertFalse(resultado)



    #############################################
    #         Pruebas para obtenerNodos         #
    #############################################

    def testObtenerNodosResultadoTamano1(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)

        nodos = oNodo.obtenerNodos()
        self.assertEqual(len(nodos),1)


    def testObtenerNodosResultadoTamano3(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        resultado2 = oNodo.crearNodo(self.nombre+str(2), 'vista', json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado3 = oNodo.crearNodoExterno(self.nombre+str(3),json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        
        nodos = oNodo.obtenerNodos()
        self.assertEqual(len(nodos),3)



    #############################################
    #       Pruebas para obtenerNodosVista      #
    #############################################

    def testObtenerNodosVistaResultadoTamano1(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(1), 'vista', json.dumps(self.propiedades), self.idDiagrama)

        nodos = oNodo.obtenerNodosVista()
        self.assertEqual(len(nodos),1)


    def testObtenerNodosVistaResultadoTamano2(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(1), 'vista', json.dumps(self.propiedades), self.idDiagrama)
        resultado2 = oNodo.crearNodo(self.nombre+str(2), 'vista', json.dumps(self.propiedades), self.idDiagrama)
        
        nodos = oNodo.obtenerNodosVista()
        self.assertEqual(len(nodos),2)



    #############################################
    #      Pruebas para obtenerNodosAccion      #
    #############################################

    def testObtenerNodosAccionResultadoTamano1(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(1), 'accion', json.dumps(self.propiedades), self.idDiagrama)

        nodos = oNodo.obtenerNodosAccion()
        self.assertEqual(len(nodos),1)


    def testObtenerNodosAccionResultadoTamano2(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(1), 'accion', json.dumps(self.propiedades), self.idDiagrama)
        resultado2 = oNodo.crearNodo(self.nombre+str(2), 'accion', json.dumps(self.propiedades), self.idDiagrama)
        
        nodos = oNodo.obtenerNodosAccion()
        self.assertEqual(len(nodos),2)



    # #############################################
    # #    Pruebas para obtenerNodosOperacion     #
    # #############################################

    # def testObtenerNodosOperacionResultadoTamano1(self):
    #     oNodo      = Nodo()
    #     resultado1 = oNodo.crearNodo(self.nombre+str(1), 'operacion', json.dumps(self.propiedades), self.idDiagrama)

    #     nodos = oNodo.obtenerNodosOperacion()
    #     self.assertEqual(len(nodos),1)


    # def testObtenerNodosOperacionResultadoTamano2(self):
    #     oNodo      = Nodo()
    #     resultado1 = oNodo.crearNodo(self.nombre+str(1), 'operacion', json.dumps(self.propiedades), self.idDiagrama)
    #     resultado2 = oNodo.crearNodo(self.nombre+str(2), 'operacion', json.dumps(self.propiedades), self.idDiagrama)
        
    #     nodos = oNodo.obtenerNodosOperacion()
    #     self.assertEqual(len(nodos),2)



    #############################################
    #     Pruebas para obtenerNodosExterno      #
    #############################################

    def testObtenerNodosExternoResultadoTamano1(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado1 = oNodo.crearNodoExterno(self.nombre+str(1), json.dumps(self.propiedades), self.idDiagrama, idNodoExt)

        nodos = oNodo.obtenerNodosExterno()
        self.assertEqual(len(nodos),1)


    def testObtenerNodosExternoResultadoTamano2(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt  = nodo[0].idNodo
        resultado1 = oNodo.crearNodoExterno(self.nombre+str(1), json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        resultado2 = oNodo.crearNodoExterno(self.nombre+str(2), json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        
        nodos = oNodo.obtenerNodosExterno()
        self.assertEqual(len(nodos),2)



    #############################################
    #          Pruebas para existeNodo          #
    #############################################

    def testExisteNodoValido(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(4), 'vista', json.dumps(self.propiedades), self.idDiagrama)
        nodo       = oNodo.obtenerNodosPorNombre(self.nombre+str(4))
        idNodo     = nodo[0].idNodo

        existe = oNodo.existeNodo(idNodo)
        self.assertTrue(existe)


    def testExisteNodoNegativo(self):
        oNodo = Nodo()
        existe  = oNodo.existeNodo(-1)
        self.assertFalse(existe)


    def testExisteNodoCero(self):
        oNodo  = Nodo()
        existe = oNodo.existeNodo(0)
        self.assertFalse(existe)


    def testExisteNodoNone(self):
        oNodo  = Nodo()
        existe = oNodo.existeNodo(None)
        self.assertFalse(existe)



    #############################################
    #     Pruebas para obtenerNodosPorNombre    #
    #############################################

    def testObtenerNodosValidoResultadoTamano1(self):
        oNodo  = Nodo() 
        creado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodos  = oNodo.obtenerNodosPorNombre(self.nombre)
        self.assertEqual(len(nodos), 1)


    def testObtenerNodosValidoResultadoTamano2(self):
        oNodo   = Nodo()  
        creado1 = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        creado1 = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodos   = oNodo.obtenerNodosPorNombre(self.nombre)
        self.assertEqual(len(nodos), 2)


    def testObtenerNodosPorNombreTamanoCero(self):
        oNodo  = Nodo() 
        creado = oNodo.crearNodo('', self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodos  = oNodo.obtenerNodosPorNombre('')
        self.assertEqual(len(nodos), 1)


    def testObtenerNodosPorNombreTamanoMaximo(self):
        oNodo  = Nodo()  
        creado = oNodo.crearNodo('X'*TAM_MAX_NOMBRE, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodos  = oNodo.obtenerNodosPorNombre('X'*TAM_MAX_NOMBRE)
        self.assertEqual(len(nodos), 1)


    def testObtenerNodosPorNombreTamanoMayorAlMaximo(self):
        oNodo  = Nodo()  
        creado = oNodo.crearNodo('X'*(TAM_MAX_NOMBRE+1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodos  = oNodo.obtenerNodosPorNombre('X'*(TAM_MAX_NOMBRE+1))
        self.assertEqual(len(nodos), 0)


    def testObtenerNodosPorNombreNone(self):
        oNodo = Nodo()  
        nodos = oNodo.obtenerNodosPorNombre(None)
        self.assertEqual(len(nodos), 0)



    #############################################
    #   Pruebas para obtenerNodosPorDiagrama    #
    #############################################

    def testObtenerNodosPorDiagramaValido(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        resultado2 = oNodo.crearNodo(self.nombre+str(2), 'vista', json.dumps(self.propiedades), self.idDiagrama)
     
        nodos = oNodo.obtenerNodosPorDiagrama(self.idDiagrama)
        self.assertEqual(len(nodos),2)


    def testObtenerNodosPorDiagramaIDCero(self):
        oNodo = Nodo()
        nodos = oNodo.obtenerNodosPorDiagrama(0)
        self.assertEqual(len(nodos),0)


    def testObtenerNodosPorDiagramaIDNegativo(self):
        oNodo = Nodo()
        nodos = oNodo.obtenerNodosPorDiagrama(-1)
        self.assertEqual(len(nodos),0)


    def testObtenerNodosPorDiagramaIDNone(self):
        oNodo = Nodo()
        nodos = oNodo.obtenerNodosPorDiagrama(None)
        self.assertEqual(len(nodos),0)



    #############################################
    #    Pruebas para obtenerNodosPorDiseno     #
    #############################################

    def testObtenerNodosPorDisenoValido(self):
        oNodo      = Nodo()
        resultado1 = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        resultado2 = oNodo.crearNodo(self.nombre+str(2), 'vista', json.dumps(self.propiedades), self.idDiagrama)
     
        nodos = oNodo.obtenerNodosPorDiseno(self.idDiagrama)
        self.assertEqual(len(nodos),2)


    def testObtenerNodosPorDisenoIDCero(self):
        oNodo = Nodo()
        nodos = oNodo.obtenerNodosPorDiseno(0)
        self.assertEqual(len(nodos),0)


    def testObtenerNodosPorDisenoIDNegativo(self):
        oNodo = Nodo()
        nodos = oNodo.obtenerNodosPorDiseno(-1)
        self.assertEqual(len(nodos),0)


    def testObtenerNodosPorDisenoIDNone(self):
        oNodo = Nodo()
        nodos = oNodo.obtenerNodosPorDiseno(None)
        self.assertEqual(len(nodos),0)



    # #############################################
    # #        Pruebas para actualizarNodo        #
    # #############################################

    # def testActualizarNodoValido(self):
    #     oNodo  = Nodo()

    #     # Creamos un nodo.
    #     creado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
    #     idNodo = nodo[0].idNodo
        
    #     # Creamos un nuevo diagrama.
    #     nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
    #     db.session.add(nuevoDiagrama)
    #     db.session.commit()
    #     diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
    #     idDiagrama = diagrama.idDiagrama

    #     # Actualizamos con los nuevos valores.
    #     actualizado = oNodo.actualizarNodo(idNodo, self.nombre+str(1), 'vista', json.dumps({'prop3': 'valor3'}), idDiagrama)
    #     self.assertTrue(actualizado)


    # def testActualizarNodoRepetido(self):
    #     oNodo  = Nodo()

    #     # Creamos un nodo.
    #     creado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
    #     idNodo = nodo[0].idNodo

    #     # Creamos un nuevo diagrama.
    #     nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
    #     db.session.add(nuevoDiagrama)
    #     db.session.commit()
    #     diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
    #     idDiagrama = diagrama.idDiagrama

    #     # Actualizamos con los nuevos valores.
    #     actualizado = oNodo.actualizarNodo(idNodo, self.nombre+str(1), 'vista', json.dumps({'prop3': 'valor3'}), idDiagrama)
    #     actualizado = oNodo.actualizarNodo(idNodo, self.nombre+str(1), 'vista', json.dumps({'prop3': 'valor3'}), idDiagrama)
    #     self.assertTrue(actualizado)


    # def testActualizarNodoIDCero(self):
    #     oNodo       = Nodo()
    #     actualizado = oNodo.actualizarNodo(0, self.nombre+str(1), self.tipo, json.dumps({'prop4': 'valor4'}), self.idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoIDNegativo(self):
    #     oNodo       = Nodo()
    #     actualizado = oNodo.actualizarNodo(-1, self.nombre+str(1), self.tipo, json.dumps({'prop4': 'valor4'}), self.idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoIDNone(self):
    #     oNodo       = Nodo()
    #     actualizado = oNodo.actualizarNodo(None, self.nombre+str(1), self.tipo, json.dumps({'prop4': 'valor4'}), self.idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoNombreTamanoCero(self):
    #     oNodo  = Nodo()

    #     # Creamos un nodo.
    #     creado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
    #     idNodo = nodo[0].idNodo

    #     # Creamos un nuevo diagrama.
    #     nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
    #     db.session.add(nuevoDiagrama)
    #     db.session.commit()
    #     diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
    #     idDiagrama = diagrama.idDiagrama

    #     # Actualizamos con los nuevos valores.
    #     actualizado = oNodo.actualizarNodo(idNodo, '', 'vista', json.dumps({'prop3': 'valor3'}), idDiagrama)
    #     self.assertTrue(actualizado)


    # def testActualizarNodoNombreTamanoMaximo(self):
    #     oNodo  = Nodo()

    #     # Creamos un nodo.
    #     creado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
    #     idNodo = nodo[0].idNodo

    #     # Creamos un nuevo diagrama.
    #     nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
    #     db.session.add(nuevoDiagrama)
    #     db.session.commit()
    #     diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
    #     idDiagrama = diagrama.idDiagrama

    #     # Actualizamos con los nuevos valores.
    #     actualizado = oNodo.actualizarNodo(idNodo, 'X'*TAM_MAX_NOMBRE, 'vista', json.dumps({'prop3': 'valor3'}), idDiagrama)
    #     self.assertTrue(actualizado)


    # def testActualizarNombreNombreTamanoMayorAlMaximo(self):
    #     oNodo  = Nodo()

    #     # Creamos un nodo.
    #     creado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
    #     idNodo = nodo[0].idNodo

    #     # Creamos un nuevo diagrama.
    #     nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
    #     db.session.add(nuevoDiagrama)
    #     db.session.commit()
    #     diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
    #     idDiagrama = diagrama.idDiagrama

    #     # Actualizamos con los nuevos valores.
    #     actualizado = oNodo.actualizarNodo(idNodo, 'X'*(TAM_MAX_NOMBRE+1), 'vista', json.dumps({'prop3': 'valor3'}), idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNombreNombreNone(self):
    #     oNodo  = Nodo()

    #     # Creamos un nodo.
    #     creado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
    #     idNodo = nodo[0].idNodo

    #     # Creamos un nuevo diagrama.
    #     nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
    #     db.session.add(nuevoDiagrama)
    #     db.session.commit()
    #     diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
    #     idDiagrama = diagrama.idDiagrama

    #     # Actualizamos con los nuevos valores.
    #     actualizado = oNodo.actualizarNodo(idNodo, None, 'vista', json.dumps({'prop3': 'valor3'}), idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoTipoNone(self):
    #     oNodo  = Nodo()

    #     # Creamos un nodo.
    #     creado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
    #     idNodo = nodo[0].idNodo

    #     # Creamos un nuevo diagrama.
    #     nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
    #     db.session.add(nuevoDiagrama)
    #     db.session.commit()
    #     diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
    #     idDiagrama = diagrama.idDiagrama

    #     # Actualizamos con los nuevos valores.
    #     actualizado = oNodo.actualizarNodo(idNodo, self.nombre+str(1), None, json.dumps({'prop3': 'valor3'}), idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoPropiedadesVacia(self):
    #     oNodo  = Nodo()

    #     # Creamos un nodo.
    #     creado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
    #     idNodo = nodo[0].idNodo

    #     # Creamos un nuevo diagrama.
    #     nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
    #     db.session.add(nuevoDiagrama)
    #     db.session.commit()
    #     diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
    #     idDiagrama = diagrama.idDiagrama
        
    #     # Actualizamos con los nuevos valores.
    #     actualizado = oNodo.actualizarNodo(idNodo, self.nombre+str(1), 'vista', json.dumps({}), idDiagrama)
    #     self.assertTrue(actualizado)


    # def testActualizarNodoPropiedadesNone(self):
    #     oNodo  = Nodo()

    #     # Creamos un nodo.
    #     creado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
    #     idNodo = nodo[0].idNodo

    #     # Creamos un nuevo diagrama.
    #     nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
    #     db.session.add(nuevoDiagrama)
    #     db.session.commit()
    #     diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
    #     idDiagrama = diagrama.idDiagrama
        
    #     # Actualizamos con los nuevos valores.
    #     actualizado = oNodo.actualizarNodo(idNodo, self.nombre+str(1), 'vista', None, idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoIDCeroNombreNone(self):
    #     oNodo       = Nodo()
    #     actualizado = oNodo.actualizarNodo(0, None, self.tipo, json.dumps({'prop4': 'valor4'}), self.idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoIDCeroTipoNone(self):
    #     oNodo       = Nodo()
    #     actualizado = oNodo.actualizarNodo(0, self.nombre, None, json.dumps({'prop4': 'valor4'}), self.idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoIDCeroPropiedadesNone(self):
    #     oNodo       = Nodo()
    #     actualizado = oNodo.actualizarNodo(0, self.nombre, self.tipo, None, self.idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoIDNoneNombreNone(self):
    #     oNodo       = Nodo()
    #     actualizado = oNodo.actualizarNodo(None, None, self.tipo, json.dumps({'prop4': 'valor4'}), self.idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoIDNoneTipoNone(self):
    #     oNodo       = Nodo()
    #     actualizado = oNodo.actualizarNodo(None, self.nombre, None, json.dumps({'prop4': 'valor4'}), self.idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoIDNonePropiedadesNone(self):
    #     oNodo       = Nodo()
    #     actualizado = oNodo.actualizarNodo(None, self.nombre, self.tipo, None, self.idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoNombreNoneTipoNone(self):
    #     oNodo  = Nodo()

    #     # Creamos un nodo.
    #     creado = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
    #     idNodo = nodo[0].idNodo

    #     # Creamos un nuevo diagrama.
    #     nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
    #     db.session.add(nuevoDiagrama)
    #     db.session.commit()
    #     diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
    #     idDiagrama = diagrama.idDiagrama

    #     # Actualizamos con los nuevos valores.
    #     actualizado = oNodo.actualizarNodo(idNodo, None, None, json.dumps({'prop3': 'valor3'}), idDiagrama)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoNombreNoneIdDiagramaNone(self):
    #     oNodo       = Nodo()

    #     # Creamos un nodo.
    #     creado      = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     nodo        = oNodo.obtenerNodosPorNombre(self.nombre)
    #     idNodo      = nodo[0].idNodo

    #     # Creamos un nuevo diagrama.
    #     nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
    #     db.session.add(nuevoDiagrama)
    #     db.session.commit()
    #     diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
    #     idDiagrama = diagrama.idDiagrama

    #     # Actualizamos con los nuevos valores.
    #     actualizado = oNodo.actualizarNodo(idNodo, None, 'vista', {'prop3':'valor3'}, None)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoTipoNoneIdDiagramaNone(self):
    #     oNodo       = Nodo()

    #     # Creamos un nodo.
    #     creado      = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
    #     nodo        = oNodo.obtenerNodosPorNombre(self.nombre)
    #     idNodo      = nodo[0].idNodo

    #     # Creamos un nuevo diagrama.
    #     nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
    #     db.session.add(nuevoDiagrama)
    #     db.session.commit()
    #     diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
    #     idDiagrama = diagrama.idDiagrama

    #     # Actualizamos con los nuevos valores.
    #     actualizado = oNodo.actualizarNodo(idNodo, self.nombre, None, {'prop3':'valor3'}, None)
    #     self.assertFalse(actualizado)


    # def testActualizarNodoArgumentosNone(self):
    #     oNodo       = Nodo()
    #     actualizado = oNodo.actualizarNodo(None, None, None, None, None)
    #     self.assertFalse(actualizado)



    #############################################
    #    Pruebas para actualizarNodoExterno     #
    #############################################

    def testActualizarNodoExternoValido(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo
        
        # Cramos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama       

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(idNodo, self.nombre+str(2), json.dumps({'prop4': 'valor4'}), idDiagrama, idNodoExt)
        self.assertTrue(actualizado)


    def testActualizarNodoExternoRepetido(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo
        
        # Cramos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(idNodo, self.nombre+str(2), json.dumps({'prop4': 'valor4'}), idDiagrama, idNodoExt)
        actualizado = oNodo.actualizarNodoExterno(idNodo, self.nombre+str(2), json.dumps({'prop4': 'valor4'}), idDiagrama, idNodoExt)
        self.assertTrue(actualizado)


    def testActualizarNodoExternoIDCero(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(0, self.nombre+str(2), json.dumps({'prop4': 'valor4'}), idDiagrama, idNodoExt)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoIDNegativo(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(-1, self.nombre+str(2), json.dumps({'prop4': 'valor4'}), idDiagrama, idNodoExt)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoIDNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(None, self.nombre+str(2), json.dumps({'prop4': 'valor4'}), idDiagrama, idNodoExt)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoNombreTamanoCero(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(idNodo, '', json.dumps({'prop4': 'valor4'}), idDiagrama, idNodoExt)
        self.assertTrue(actualizado)


    def testActualizarNodoExternoNombreTamanoMaximo(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(idNodo, 'X'*TAM_MAX_NOMBRE, json.dumps({'prop4': 'valor4'}), idDiagrama, idNodoExt)
        self.assertTrue(actualizado)


    def testActualizarNodoExternoNombreTamanoMayorAlMaximo(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(idNodo, 'X'*(TAM_MAX_NOMBRE+1), json.dumps({'prop4': 'valor4'}), idDiagrama, idNodoExt)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoNombreNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(idNodo, None, json.dumps({'prop4': 'valor4'}), idDiagrama, idNodoExt)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoPropiedadesVacia(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(idNodo, self.nombre+str(2), json.dumps({}), idDiagrama, idNodoExt)
        self.assertTrue(actualizado)


    def testActualizarNodoExternoPropiedadesNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(idNodo, self.nombre+str(2), None, idDiagrama, idNodoExt)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoIdNodoExtNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(idNodo, self.nombre+str(2), json.dumps({'prop4': 'valor4'}), idDiagrama, None)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoIDCeroNombreNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(0, None, json.dumps({'prop4': 'valor4'}), idDiagrama, idNodoExt)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoIDCeroIdNodoExtNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(0, self.nombre+str(2), json.dumps({'prop4': 'valor4'}), idDiagrama, None)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoIDCeroPropiedadesNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(0, self.nombre+str(2), None, idDiagrama, idNodoExt)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoIDNoneNombreNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(None, None, json.dumps({'prop4': 'valor4'}), idDiagrama, idNodoExt)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoIDNoneIdNodoExtNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(None, self.nombre+str(2), json.dumps({'prop4': 'valor4'}), idDiagrama, None)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoIDNonePropiedadesNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(None, self.nombre+str(2), None, idDiagrama, idNodoExt)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoNombreNoneIdNodoExtNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(idNodo, None, json.dumps({'prop4': 'valor4'}), idDiagrama, None)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoNombreNoneIdDiagramaNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(idNodo, None, json.dumps({'prop4': 'valor4'}), None, idNodoExt)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoIdNodoExtNoneIdDiagramaNone(self):
        oNodo     = Nodo()

        # Creamos un nodo.
        creado    = oNodo.crearNodo(self.nombre+str(1), self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre+str(1))
        idNodoExt = nodo[0].idNodo

        # Creamos un nodo externo.
        creado = oNodo.crearNodoExterno(self.nombre, json.dumps(self.propiedades), self.idDiagrama, idNodoExt)
        nodo   = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo = nodo[0].idNodo

        # Creamos un nuevo diagrama.
        nuevoDiagrama = clsDiagrama('Diagrama2', 'Diagrama para modulo de login', json.dumps(self.propiedades), self.idDiseno)
        db.session.add(nuevoDiagrama)
        db.session.commit()
        diagrama   = clsDiagrama.query.filter_by(nombre='Diagrama2').first()
        idDiagrama = diagrama.idDiagrama

        # Actualizamos el nodo externo.
        actualizado = oNodo.actualizarNodoExterno(idNodo, self.nombre+str(2), json.dumps({'prop4': 'valor4'}), None, None)
        self.assertFalse(actualizado)


    def testActualizarNodoExternoArgumentosNone(self):
        oNodo       = Nodo()
        actualizado = oNodo.actualizarNodo(None, None, None, None, None)
        self.assertFalse(actualizado)



    #############################################
    #        Pruebas para eliminarNodo          #
    #############################################

    def testEliminarNodoValido(self):
        oNodo     = Nodo()
        creado    = oNodo.crearNodo(self.nombre, self.tipo, json.dumps(self.propiedades), self.idDiagrama)
        nodo      = oNodo.obtenerNodosPorNombre(self.nombre)
        idNodo    = nodo[0].idNodo
        eliminado = oNodo.eliminarNodo(idNodo)
        self.assertTrue(eliminado)


    def testEliminarDisenoIDCero(self):
        oNodo     = Nodo()
        eliminado = oNodo.eliminarNodo(0)
        self.assertFalse(eliminado)


    def testEliminarDisenoIDNegativo(self):
        oNodo     = Nodo()
        eliminado = oNodo.eliminarNodo(-1)
        self.assertFalse(eliminado)


    def testEliminarDisenoIDNone(self):
        oNodo     = Nodo()
        eliminado = oNodo.eliminarNodo(None)
        self.assertFalse(eliminado)