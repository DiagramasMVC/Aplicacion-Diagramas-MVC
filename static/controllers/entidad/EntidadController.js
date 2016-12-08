mvcModule.config(function ($routeProvider) {
    $routeProvider.when('/VEntidad/:idEntidad', {
                controller: 'VEntidadController',
                templateUrl: 'static/views/entidad/VEntidad.html'
            }).when('/VCrearEntidad/:idDiseno', {
                controller: 'VCrearEntidadController',
                templateUrl: 'static/views/entidad/VCrearEntidad.html'
            });
});


mvcModule.controller('VEntidadController', 
   ['$scope', 
    '$location', 
    '$route', 
    'flash', 
    '$routeParams',
    'entidadService',
    'disenoService', 
    'diagramaService',
    'identificarService',
    function ($scope, $location, $route, flash, $routeParams, entidadService, disenoService, diagramaService, identificarService) {
        $scope.msg = '';
        $scope.fEntidad = {};

        entidadService.VEntidad({"idEntidad":$routeParams.idEntidad}).then(function (object) {
            $scope.res = object.data;
            for (var key in object.data) {
                $scope[key] = object.data[key];
            }
            if ($scope.logout) {
                $location.path('/');
            }
        });
        $scope.VDiseno1 = function(idDiseno) {
            $location.path('/VDiseno/'+idDiseno);
        };
        $scope.VLogin1 = function() {
            $location.path('VLogin');
        };
        $scope.AEliminarEntidad1 = function(idEntidad) {

            entidadService.AEliminarEntidad({"idEntidad":((typeof idEntidad === 'object')?JSON.stringify(idEntidad):idEntidad)}).then(function (object) {
                var msg = object.data["msg"];
                if (msg) flash(msg);
                var label = object.data["label"];
                $location.path(label);
                $route.reload();
            });
        };

        $scope.fEntidadSubmitted = false;
        $scope.AModificarEntidad1 = function(isValid) {
            $scope.fEntidadSubmitted = true;
            if (isValid) {

                entidadService.AModificarEntidad($scope.fEntidad).then(function (object) {
                    var msg = object.data["msg"];
                    if (msg) flash(msg);
                    var label = object.data["label"];
                    $location.path(label);
                    $route.reload();
                });
            }
        };        

    }]
);



mvcModule.controller('VCrearEntidadController', 
   ['$scope', 
    '$location', 
    '$route', 
    'flash', 
    '$routeParams',
    'entidadService',
    'disenoService', 
    'diagramaService',
    'identificarService',
    function ($scope, $location, $route, flash, $routeParams, entidadService, disenoService, diagramaService, identificarService) {
        $scope.msg = '';
        $scope.fEntidad = {};

        entidadService.VCrearEntidad({"idDiseno":$routeParams.idDiseno}).then(function (object) {
            $scope.res = object.data;
            for (var key in object.data) {
                $scope[key] = object.data[key];
            }
            if ($scope.logout) {
                $location.path('/');
            }
        });

        $scope.VDiseno2 = function(idDiseno) {
            $location.path('/VDiseno/'+idDiseno);
         };
        $scope.VLogin2 = function() {
            $location.path('/VLogin');
        };

        $scope.fEntidadSubmitted = false;
        $scope.ACrearEntidad1 = function(isValid) {
            $scope.fEntidadSubmitted = true;
            if (isValid) {
              
                entidadService.ACrearEntidad($scope.fEntidad).then(function (object) {
                    var msg = object.data["msg"];
                    if (msg) flash(msg);
                    var label = object.data["label"];
                    $location.path(label);
                    $route.reload();
                });
            }
        };
    }]
);
