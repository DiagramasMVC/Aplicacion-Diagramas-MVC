mvcModule.config(function ($routeProvider) {
    $routeProvider.when('/VVista/:idVista', {
                controller: 'VVistaController',
                templateUrl: 'static/views/elemento/VVista.html'
            }).when('/VAccion/:idAccion', {
                controller: 'VAccionController',
                templateUrl: 'static/views/elemento/VAccion.html'
            }).when('/VOperacion/:idOperacion', {
                controller: 'VOperacionController',
                templateUrl: 'static/views/elemento/VOperacion.html'
            }).when('/VCrearElemento/:idDiagrama', {
                controller: 'VCrearElementoController',
                templateUrl: 'static/views/elemento/VCrearElemento.html'
            });
});


mvcModule.controller('VVistaController', [
    '$scope', 
    '$location', 
    '$route',
    'flash',
    '$routeParams',
    'ngTableParams',
    'elementoService',
    'disenoService',
    'diagramaService',
    'identificarService',
    function ($scope, $location, $route, flash, $routeParams, ngTableParams, elementoService, disenoService, diagramaService, identificarService) {
        $scope.msg = '';
        $scope.fVista = {};
        
        elementoService.VVista({"idVista":$routeParams.idVista}).then(function (object) {
            $scope.res = object.data;
            for (var key in object.data) {
                $scope[key] = object.data[key];
            }
            if ($scope.logout) {
                $location.path('/');
            }
        });
        $scope.VDiagrama1 = function(idDiagrama) {
            $location.path('/VDiagrama/'+idDiagrama);
        };
        $scope.VLogin1 = function() {
            $location.path('/VLogin');
        };
        $scope.VDibujo1 = function(idDiagrama) {
            $location.path('/VDiagramas/'+idDiagrama)
        };

        $scope.fVistaSubmitted = false;
        $scope.AModificarVista1 = function(isValid) {
            $scope.fVistaSubmitted = true;
            if (isValid) {

                elementoService.AModificarVista($scope.fVista).then(function (object) {
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


mvcModule.controller('VAccionController', [
    '$scope', 
    '$location', 
    '$route',
    'flash',
    '$routeParams',
    'ngTableParams',
    'elementoService',
    'disenoService',
    'diagramaService',
    'identificarService',
    function ($scope, $location, $route, flash, $routeParams, ngTableParams, elementoService, disenoService, diagramaService, identificarService) {
        $scope.msg = '';
        $scope.fAccion = {};
        
        elementoService.VAccion({"idAccion":$routeParams.idAccion}).then(function (object) {
            $scope.res = object.data;
            for (var key in object.data) {
                $scope[key] = object.data[key];
            }
            if ($scope.logout) {
                $location.path('/');
            }
        });
        $scope.VDiagrama2 = function(idDiagrama) {
            $location.path('/VDiagrama/'+idDiagrama);
        };
        $scope.VLogin2 = function() {
            $location.path('/VLogin');
        };
        $scope.fAccionSubmitted = false;
        $scope.AModificarAccion1 = function(isValid) {
            $scope.fAccionSubmitted = true;
            if (isValid) {

                elementoService.AModificarAccion($scope.fAccion).then(function (object) {
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


mvcModule.controller('VOperacionController', [
    '$scope', 
    '$location', 
    '$route',
    'flash',
    '$routeParams',
    'ngTableParams',
    'elementoService',
    'disenoService',
    'diagramaService',
    'identificarService',
    function ($scope, $location, $route, flash, $routeParams, ngTableParams, elementoService, disenoService, diagramaService, identificarService) {
        $scope.msg = '';
        $scope.fOperacion = {};
        
        elementoService.VOperacion({"idOperacion":$routeParams.idOperacion}).then(function (object) {
            $scope.res = object.data;
            for (var key in object.data) {
                $scope[key] = object.data[key];
            }
            if ($scope.logout) {
                $location.path('/');
            }
        });
        $scope.VDiagrama3 = function(idDiagrama) {
            $location.path('/VDiagrama/'+idDiagrama);
        };
        $scope.VLogin3 = function() {
            $location.path('/VLogin');
        };
        $scope.fOperacionSubmitted = false;
        $scope.AModificarOperacion1 = function(isValid) {
            $scope.fOperacionSubmitted = true;
            if (isValid) {

                elementoService.AModificarOperacion($scope.fOperacion).then(function (object) {
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


mvcModule.controller('VCrearElementoController', [
    '$scope', 
    '$location', 
    '$route',
    'flash',
    '$routeParams',
    'ngTableParams',
    'elementoService',
    'disenoService',
    'diagramaService',
    'identificarService',
    function ($scope, $location, $route, flash, $routeParams, ngTableParams, elementoService, disenoService, diagramaService, identificarService) {
        $scope.msg = '';
        $scope.fElemento = {};
        $scope.fElemento.atributos = [];

        elementoService.VCrearElemento({"idDiagrama":$routeParams.idDiagrama}).then(function (object) {
            $scope.res = object.data;
            for (var key in object.data) {
                $scope[key] = object.data[key];
            }
            if ($scope.logout) {
                $location.path('/');
            }
        });
        $scope.VDiagrama4 = function(idDiagrama) {
            $location.path('/VDiagrama/'+idDiagrama);
        };
        $scope.VLogin4 = function() {
            $location.path('/VLogin');
        };

        $scope.fElementoSubmitted = false;
        $scope.ACrearElemento1 = function(isValid) {
            $scope.fElementoSubmitted = true;
            if (isValid) {

                elementoService.ACrearElemento($scope.fElemento).then(function (object) {
                    var msg = object.data["msg"];
                    if (msg) flash(msg);
                    var label = object.data["label"];
                    $location.path(label);
                    $route.reload();
                });
            }
        };

        $scope.agregar1 = function() {

            $scope.fElemento.atributos.push($scope.fElemento.nombre_atributo);
            $scope.fElemento.nombre_atributo = '';
        };
    }]
);