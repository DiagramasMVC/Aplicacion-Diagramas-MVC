mvcModule.service('identificarService', ['$q', '$http', 
	function($sq, $http) {

		this.AIdentificar = function(fLogin) {
			return $http({
				url: 'identificar/AIdentificar',
				data: fLogin,
				method: 'POST',
			});
		};

		this.VLogin = function(args) {
			if (typeof args == 'undefined') args={};
			return $http({
				url: 'identificar/VLogin',
				method: 'GET',
				params: args
			});
		};

		this.ARegistrar = function(fUsuario) {
			return $http({
				url: "identificar/ARegistrar",
				data: fUsuario,
				method: 'POST',
			});
		};

		this.VRegistro = function(args) {
			if (typeof args == 'undefined') args={};
			return $http({
				url:'identificar/VRegistro',
				method: 'GET',
				params: args
			});
		};
}]);