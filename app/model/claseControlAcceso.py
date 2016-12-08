# -*- coding: utf-8 -*-.

# DESCRIPCION: Modulo donde se definen las funciones relacionadas al acceso 
#              a la aplicación.

import uuid
import hashlib
import re

# Declaración de constantes.
TAM_MIN_CLAVE = 8
TAM_MAX_CLAVE = 16


class ControlAcceso(object):
    """Permite manejar de manera privada la clave asociada a un usuario."""
    
    def __init__(self):
        ohast=''
        self.expresionRegular = ('(([a-z]|[A-Z]|\d|[@.#$+*])*[@.#$+*]([a-z]|[A-Z]|\d|[@.#$+*])*[A-Z]([a-z]|[A-Z]|\d|[@.#$+*])*\d([a-z]|[A-Z]|\d|[@.#$+*])*)|'
                                  '(([a-z]|[A-Z]|\d|[@.#$+*])*[@.#$+*]([a-z]|[A-Z]|\d|[@.#$+*])*\d([a-z]|[A-Z]|\d|[@.#$+*])*[A-Z]([a-z]|[A-Z]|\d|[@.#$+*])*)|'
                                  '(([a-z]|[A-Z]|\d|[@.#$+*])*[A-Z]([a-z]|[A-Z]|\d|[@.#$+*])*[@.#$+*]([a-z]|[A-Z]|\d|[@.#$+*])*\d([a-z]|[A-Z]|\d|[@.#$+*])*)|'
                                  '(([a-z]|[A-Z]|\d|[@.#$+*])*[A-Z]([a-z]|[A-Z]|\d|[@.#$+*])*\d([a-z]|[A-Z]|\d|[@.#$+*])*[@.#$+*]([a-z]|[A-Z]|\d|[@.#$+*])*)|'
                                  '(([a-z]|[A-Z]|\d|[@.#$+*])*\d([a-z]|[A-Z]|\d|[@.#$+*])*[@.#$+*]([a-z]|[A-Z]|\d|[@.#$+*])*[A-Z]([a-z]|[A-Z]|\d|[@.#$+*])*)|'
                                  '(([a-z]|[A-Z]|\d|[@.#$+*])*\d([a-z]|[A-Z]|\d|[@.#$+*])*[A-Z]([a-z]|[A-Z]|\d|[@.#$+*])*[@.#$+*]([a-z]|[A-Z]|\d|[@.#$+*])*)')


    def claveValida(self, clave):
        """Permite saber si una clave es válida."""
        tamanoClave   = len(clave) 
        esClaveValida = False
                    
        if tamanoClave >= MIN_TAM_CLAVE and tamanoClave <= MAX_TAM_CLAVE:
            esClaveValida = re.search(self.expresionRegular,clave)
            esClaveValida = True
           
        return esClaveValida


    def encriptarClave(self, clave):
        '''Permite encriptar una clave dada'''

        oHash = ""
        #Verificamos la longitud de la clave.
        tamanoClave = len(clave)
        
        if tamanoClave >= MIN_TAM_CLAVE and tamanoClave <= MAX_TAM_CLAVE:
            esClaveValida = re.search(self.expresionRegular, clave)
            
            if esClaveValida:

                # uuid es usado para generar numeros random
                salt = uuid.uuid4().hex

                # hash
                oHash= hashlib.sha256(salt.encode() + clave.encode()).hexdigest() + ':' + salt
                return oHash
            else:
                return oHash
        else:
            return oHash 


    def verificarClave(self, claveEncriptada, claveAVerificar):
        '''Permite comprobar si una clave encriptada corresponde a una clave dada'''

        # Verificamos la longitud de la clave
        tamanoClave = len(claveAVerificar) 
               
        if tamanoClave >= MIN_TAM_CLAVE and tamanoClave <= MAX_TAM_CLAVE:
            esClaveValida = re.search(self.expresionRegular, claveAVerificar) 
            
            if esClaveValida:
                claveEncriptada, salt = claveEncriptada.split(':')
                return claveEncriptada == hashlib.sha256(salt.encode() + claveAVerificar.encode()).hexdigest()
            else:
                return False
        else:
            return False