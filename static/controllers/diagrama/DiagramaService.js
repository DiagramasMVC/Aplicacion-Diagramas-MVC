mvcModule.service('diagramaService', ['$q', '$http', function($sq, $http) {

	this.VDiagrama = function(args) {
		if(typeof args == 'undifined') args={};
		return $http({
			url: 'diagrama/VDiagrama',
			method: 'GET',
			params: args,
		});
	};

	this.ACrearDiagrama = function(fDiagrama) {
		return $http({
			url: "diagrama/ACrearDiagrama",
			data: fDiagrama,
			method: 'POST',
		});
	};
	
	this.AModificarDiagrama = function(fDiagrama) {
		return $http({
			url: "diagrama/AModificarDiagrama",
			data: fDiagrama,
			method: 'POST',
		});
	};

    this.AEliminarDiagrama = function(args) {
      if(typeof args == 'undefined') args={};
      return $http({
        url: 'diagrama/AEliminarDiagrama',
        method: 'GET',
        params: args,
      });
    };

	this.AGuardarPosicionDiagrama = function(fDiagrama) {
		return $http({
			url: 'diagrama/AGuardarPosicionDiagrama',
			data: fDiagrama,
			method: 'POST',
		});
	};
	
}]);