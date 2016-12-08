mvcModule.service('disenoService', ['$q', '$http', function($q, $http) {

    this.VDisenos = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'diseno/VDisenos',
          method: 'GET',
          params: args
        });
    };

    this.VDiseno = function(args) {
        if(typeof args == 'undefined') args={};
        return $http({
          url: 'diseno/VDiseno',
          method: 'GET',
          params: args,
        });
    };

    this.ACrearDiseno = function(fDiseno) {
        return  $http({
          url: "diseno/ACrearDiseno",
          data: fDiseno,
          method: 'POST',
        });
    };

    this.AModificarDiseno = function(fDiseno) {
        return  $http({
          url: "diseno/AModificarDiseno",
          data: fDiseno,
          method: 'POST',
        });
    };

    this.AEliminarDiseno = function(args) {
      if(typeof args == 'undefined') args={};
      return $http({
        url: 'diseno/AEliminarDiseno',
        method: 'GET',
        params: args,
      });
    };

}]);