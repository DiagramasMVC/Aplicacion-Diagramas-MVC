mvcModule.service('elementoService', ['$q', '$http', function($sq, $http) {

		this.AModificarVista = function(fVista) {
			return $http({
				url: 'elemento/AModificarVista',
				data: fVista,
				method: 'POST',
			});
		};

		this.AModificarAccion = function(fAccion) {
			return $http({
				url: 'elemento/AModificarAccion',
				data: fAccion,
				method: 'POST',
			});
		};

		this.AModificarOperacion = function(fOperacion) {
			return $http({
				url: 'elemento/AModificarOperacion',
				data: fOperacion,
				method: 'POST',
			});
		};

		this.ACrearElemento= function(fElemento) {
			return $http({
				url: "elemento/ACrearElemento",
				data: fElemento,
				method: 'POST',
			});
		};

		this.AEliminarElemento = function(args) {
			if(typeof args == 'undefined') args={};
			return $http({
				url: 'elemento/AEliminarElemento',
				method: 'GET',
				params: args
			});
		};
}]);