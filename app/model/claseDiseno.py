# -*- coding: utf-8 -*-.

# DESCRIPCION: Modulo donde se definen las funciones relacionadas a los 
#              disenos.


# Se importan las librerias necesarias.
from modelo import *

# Declaracion de constantes.
TAM_MAX_NOMBRE = 64
NUM_MIN_ID = 1


class Diseno(object):
    """Interfaz que permite manejar los disenos de la aplicacion"""
    
    def crearDiseno(self, nombre, descripcion, idCreador, propiedades):
        """Permite insertar un nuevo diseno en la base de datos.

           Recibe:
           nombre      -- nombre del diseno a crear.
           descripcion -- descripcion del diseno a crear.
           propiedades -- archivo .json con las propiedades.

           Devuelve:
           bool -- confirma si se realizo o no la insercion.
        """
        if nombre != None and descripcion != None and idCreador != None and propiedades != None:

            tamNombre = len(nombre) <= TAM_MAX_NOMBRE
            idCreador_valido = idCreador >= NUM_MIN_ID

            if tamNombre and idCreador_valido:
                nuevoDiseno = clsDiseno(nombre, descripcion, idCreador, propiedades)
                db.session.add(nuevoDiseno)
                db.session.commit()
                return True

        return False


    def asociarDisenoAUsuario(self, idDiseno, idUsuario):
        """Permite """
        idDiseno_valido  = idDiseno >= NUM_MIN_ID
        idUsuario_valido = idUsuario >= NUM_MIN_ID

        if idDiseno_valido and idUsuario_valido:
          # Buscamos los elementos.
          diseno  = clsDiseno.query.filter_by(idDiseno=idDiseno)
          usuario = clsUsuario.query.filter_by(idUsuario=idUsuario)

          if diseno and usuario:
            # Establecemos la asociacion.
            nuevoAsoc = clsDisenosAsociadosUsuario(idDiseno, idUsuario)
            db.session.add(nuevoAsoc)
            db.session.commit()
            return True

        return False


    def obtenerDisenos(self):
        """Permite obtener todos los disenos almacenados en la base de datos
           
           Recibe:
           Ningun argumento.

           Devuelve: 
           [<idDiseno, nombre, descripcion, propiedades>] -- lista de tuplas 
           correspondientes a clsDiseno. En caso de no existir disenos devuelve 
           lista vacia.
        """
        disenos = clsDiseno.query.all()

        return disenos


    def existeDiseno(self, idDiseno):
        """Permite saber si un diseno se encuentra almacenado en la base de 
           datos o no.

           Recibe:
           idDiseno -- identificador del diseno en la tabla diseno.

           Devuelve:
           bool -- confirma si existe o no el elemento.
        """
        existeDiseno = None

        if idDiseno != None:

            if idDiseno >= NUM_MIN_ID:
                existeDiseno = clsDiseno.query.filter_by(idDiseno=idDiseno).first()

        return (existeDiseno != None)


    def obtenerDisenoPorID(self, idDiseno):
        """Permite obtener un diseno buscando por su identificador
            
           Recibe:
           idDiseno -- identificador del diseno en la tabla diseno.

           Devuelve:
           <idDiseno, nombre, descripcion, propiedades> -- tupla de la tabla 
           clsDiseno. En caso de no existir devuelve None.
        """
        existeDiseno = False

        if idDiseno != None:

            if idDiseno >= NUM_MIN_ID:
                    
                existeDiseno = clsDiseno.query.filter_by(idDiseno=idDiseno).first()

        return existeDiseno


    def obtenerDisenosPorNombre(self, nombre):
        """Permite obtener disenos por su nombre. El nombre no es unico.
           
           Recibe:
           nombre -- nombre del diseno a buscar.

           Devuelve:
           [<idDiseno, nombre, descripcion, propiedades>] -- lista de tuplas 
           correspondientes a clsDiseno. En caso de no existir disenos devuelve 
           lista vacia.
        """
        disenos = clsDiseno.query.filter_by(nombre=nombre).all()

        return disenos        


    def obtenerDisenosPorNombreYDescripcion(self, nombre, descripcion):
        """Permite obtener disenos por su nombre y descripcion. 
           El nombre no es unico y la descripcion tampoco.
           
           Recibe:
           nombre -- nombre del diseno a crear.
           descripcion -- descripcion del diseno a crear.

           Devuelve:
           [<idDiseno, nombre, descripcion, propiedades>] -- lista de tuplas 
           correspondientes a clsDiseno. En caso de no existir disenos devuelve 
           lista vacia.
        """
        disenos = clsDiseno.query.filter_by(nombre=nombre, descripcion=descripcion).all()

        return disenos


    def obtenerDisenosPorUsuario(self, idUsuario):
        """Permite obtener los disenos asociados a un usuario dado. 
           Incluye los disenos creados por dicho usuario.

           Recibe:
           idUsuario -- identificador del usuario en la tabla de usuarios.

           Devuelve:
           [<idDiseno, nombre, descripcion, propiedades>] -- lista de tuplas 
           correspondientes a clsDiseno. En caso de no existir disenos devuelve 
           lista vacia.
        """
        disenos = []
        # Obtenemos los diseños que ha creado.
        idDisenosCreados = clsDiseno.query.filter_by(idCreador=idUsuario).all()

        disenos += idDisenosCreados

        # Obtenemos los disenos a los cuales se le asoció.
        idDisenos = clsDisenosAsociadosUsuario.query.filter_by(idUsuario=idUsuario).all()
        
        for d in idDisenos:
          diseno = clsDiseno.query.filter_by(idDiseno=d).first()
          if diseno:
            disenos.append(diseno)

        return disenos


    def actualizarDiseno(self, idDiseno, nuevoNombre, nuevaDescripcion, nuevasPropiedades):
        """Permite actualizar el valor de los campos de un diseno
			
		       Recibe:
		       idDiseno          -- identificador del diseno en la tabla diseno.
               nuevoNombre       -- nuevo nombre a actualizar.
               nuevaDescripcion  -- nueva descripcion a actualizar.
               nuevasPropiedades -- archivo .json con las propiedades a actualizar.

		       Devuelve:
		       bool -- confirma si se actualizo o no el elemento.
        """
        if idDiseno != None:

          if idDiseno >= NUM_MIN_ID:

            viejoDiseno = clsDiseno.query.filter_by(idDiseno=idDiseno).first()

            if viejoDiseno != None:

              if nuevoNombre != None and nuevaDescripcion != None and nuevasPropiedades != None:

                if len(nuevoNombre) <= TAM_MAX_NOMBRE:
                
                  viejoDiseno.nombre      = nuevoNombre
                  viejoDiseno.descripcion = nuevaDescripcion
                  viejoDiseno.propiedades = nuevasPropiedades
                  db.session.commit()
                  return True

        return False
        

    def eliminarDisenoPorID(self, idDiseno):
        """Permite eliminar un diseno almacenado
		   
		       Recibe:
		       idDiseno -- identificador del diseno en la tabla diseno.

		       Devuelve:
		       bool -- confirma si se elimino o no el elemento.
        """
        if idDiseno != None:

          if idDiseno >= NUM_MIN_ID:

            diseno = clsDiseno.query.filter_by(idDiseno=idDiseno).first()

            if diseno != None:
            	db.session.delete(diseno)
            	db.session.commit()
            	return True

        return False
        

#Fin Clase Diseno

		