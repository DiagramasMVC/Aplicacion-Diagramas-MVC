mvcModule.service('entidadService', ['$q', '$http', function($q, $http) {

        this.AModificarEntidad = function(fEntidad) {
            return  $http({
              url: "entidad/AModificarEntidad",
              data: fEntidad,
              method: 'POST',
            });
        };

        this.ACrearEntidad = function(fEntidad) {
            return  $http({
              url: "entidad/ACrearEntidad",
              data: fEntidad,
              method: 'POST',
            });
        };

        this.AEliminarEntidad = function(args) {
          if(typeof args == 'undefined') args={};
          return $http({
            url: 'entidad/AEliminarEntidad',
            method: 'GET',
            params: args,
          });
        };

}]);