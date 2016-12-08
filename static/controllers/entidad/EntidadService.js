mvcModule.service('entidadService', ['$q', '$http', function($q, $http) {

        this.AModificarEntidad = function(fEntidad) {
            return  $http({
              url: "entidad/AModificarEntidad",
              data: fEntidad,
              method: 'POST',
            });
        };

        this.VEntidad = function(args) {
            if(typeof args == 'undefined') args={};
            return $http({
              url: 'entidad/VEntidad',
              method: 'GET',
              params: args,
            });
        };

        this.ACrearEntidad = function(fEntidad) {
            return  $http({
              url: "entidad/ACrearEntidad",
              data: fEntidad,
              method: 'POST',
            });
        };

        this.VCrearEntidad = function(args) {
          if(typeof args == 'undifined') args={};
          return $http({
            url: 'entidad/VCrearEntidad',
            method: 'GET',
            params: args,
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