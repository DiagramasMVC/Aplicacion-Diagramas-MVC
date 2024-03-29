mvcModule.config(function ($routeProvider) {
    $routeProvider.when('/VDisenos', {
                controller: 'VDisenosController',
                templateUrl: 'static/views/diseno/VDisenos.html'
            }).when('/VDiseno/:idDiseno', {
                controller: 'VDisenoController',
                templateUrl: 'static/views/diseno/VDiseno.html'
            });
});


mvcModule.controller('VDisenosController', 
   ['$scope', 
    '$location', 
    '$route', 
    'flash', 
    'ngTableParams',
    'disenoService', 
    'identificarService',
    function ($scope, $location, $route, flash, ngTableParams, disenoService, identificarService) {
        $scope.msg = '';
        $scope.tab = 2;
        $scope.seleccionado = 0;

        disenoService.VDisenos().then(function (object) {
            $scope.res = object.data;
            for (var key in object.data) {
                $scope[key] = object.data[key];
            }
            if ($scope.logout) {
                $location.path('/');
            }

            var VDiseno0Data = $scope.res.data0;
            if(typeof VDiseno0Data === 'undefined') VDiseno0Data=[];
            $scope.tableParams0 = new ngTableParams({
                page: 1,            // show first page
                count: 10           // count per page
            }, {
                total: VDiseno0Data.length, // length of data
                getData: function($defer, params) {
                    $defer.resolve(VDiseno0Data.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                }
            });          
        });
        $scope.elemento_eliminar_id = 0;
        $scope.setDiseno = function(id) {
            // Buscamos el diseno seleccionado.
            var i = 0; 
            var encontrado = false;

            while(i < $scope.res.data0.length) {
                if ($scope.res.data0[i].idDiseno == id) {
                    var x = $scope.res.data0[i];
                    $scope.fDiseno = {"idDiseno": x.idDiseno, "descripcion":x.descripcion, "nombre":x.nombre};
                    encontrado = true;
                }
                i++;
            }
            $scope.elemento_eliminar_id = id
            $scope.setTab(1);
            $scope.seleccionado = 1;
        };
        $scope.setTab = function(newTab) {
            $scope.tab = newTab;
        };
        $scope.isSet = function(tabNum) {
            return $scope.tab === tabNum;
        };
        $scope.VLogin1 = function() {
            $location.path('/VLogin');
        };
        $scope.VDiseno1 = function(idDiseno) {
            $location.path('/VDiseno/'+((typeof idDiseno === 'object')?JSON.stringify(idDiseno):idDiseno));
        };
        $scope.fDiseno1Submitted = false;
        $scope.ACrearDiseno1 = function(isValid) {
            $scope.fDiseno1Submitted = true;
            if (isValid) {
          
                disenoService.ACrearDiseno($scope.fDiseno1).then(function (object) {
                    var msg = object.data["msg"];
                    if (msg) flash(msg);
                    var label = object.data["label"];
                    $location.path(label);
                    $route.reload();
                });
            }
        };
        $scope.fDisenoSubmitted = false;
        $scope.AModificarDiseno1 = function(isValid) {
            $scope.fDisenoSubmitted = true;
            if (isValid) {
              
                disenoService.AModificarDiseno($scope.fDiseno).then(function (object) {
                    var msg = object.data["msg"];
                    if (msg) flash(msg);
                    var label = object.data["label"];
                    $location.path(label);
                    $route.reload();
                });
            }
        };
        $scope.AEliminarDiseno1 = function(idDiseno) {
            disenoService.AEliminarDiseno({'idDiseno':((typeof idDiseno === 'object')?JSON.stringify(idDiseno):idDiseno)}).then(function (object) {
                var msg = object.data["msg"];
                if (msg) flash(msg);
                var label = object.data["label"];
                $location.path(label);
                $route.reload();
            });
        };
    }]
);


mvcModule.controller('VDisenoController', 
   ['$scope', 
    '$location', 
    '$route', 
    'flash', 
    '$routeParams', 
    'ngTableParams',
    'disenoService', 
    'diagramaService',
    'entidadService',
    'identificarService',
    function ($scope, $location, $route, flash, $routeParams, ngTableParams, disenoService, diagramaService, entidadService, identificarService) {
        $scope.msg = '';
        $scope.tab = 2;
        $scope.fDiseno = {};
        $scope.fEntidad = {};
        $scope.seleccionado = 0;

        disenoService.VDiseno({"idDiseno":$routeParams.idDiseno}).then(function (object) {
            $scope.res = object.data;
            $scope.disenoId = $routeParams.nombreDiseno;
            for (var key in object.data) {
                $scope[key] = object.data[key];
            }
            if ($scope.logout) {
                $location.path('/');
            }
            
            var VDiagrama1Data = $scope.res.data1;
            if(typeof VDiagrama1Data === 'undefined') VDiagrama1Data=[];
                $scope.tableParams1 = new ngTableParams({
                    page: 1,            // show first page
                    count: 10           // count per page
            }, {
                    total: VDiagrama1Data.length, // length of data
                    getData: function($defer, params) {
                        $defer.resolve(VDiagrama1Data.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                    }
            });  
            
            var VEntidad1Data = $scope.res.data2;
            if(typeof VEntidad1Data === 'undefined') VEntidad1Data=[];
                $scope.tableParams2 = new ngTableParams({
                    page: 1,
                    count: 10
            }, {
                    total: VEntidad1Data.length, // length of data
                    getData: function($defer, params) {
                        $defer.resolve(VEntidad1Data.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                    }
            });
        });
        $scope.elemento_eliminar_id = 0;
        $scope.setEntidad = function(id) {
            // Buscamos el diseno seleccionado.
            var i = 0; 
            var encontrado = false;

            while(i < $scope.res.data2.length) {
                if ($scope.res.data2[i].idEntidad == id) {
                    var x = $scope.res.data2[i];
                    $scope.fEntidad1= {"idEntidad": x.idEntidad, "nombre":x.nombre};
                    encontrado = true;
                }
                i++;
            }
            $scope.elemento_eliminar_id = id;
            $scope.setTab(1);
            $scope.seleccionado = 2;
        }
        $scope.setDiagrama = function(id) {
            // Buscamos el diseno seleccionado.
            var i = 0; 
            var encontrado = false;

            while(i < $scope.res.data1.length) {
                if ($scope.res.data1[i].idDiagrama== id) {
                    var x = $scope.res.data1[i];
                    $scope.fDiagrama1 = {"idDiagrama": x.idDiagrama, "descripcion":x.descripcion, "nombre":x.nombre};
                    encontrado = true;
                }
                i++;
            }
            $scope.elemento_eliminar_id = id;
            $scope.setTab(1);
            $scope.seleccionado = 1;
        };
        $scope.setTab = function(newTab) {
            $scope.tab = newTab;
        };
        $scope.isSet = function(tabNum) {
            return $scope.tab === tabNum;
        };
        $scope.VDisenos1 = function() {
            $location.path('/VDisenos');
        };
        $scope.VLogin2 = function() {
            $location.path('/VLogin');
        };
        $scope.fDiagramaSubmitted = false;
        $scope.ACrearDiagrama1 = function(isValid) {
        $scope.fDiagramaSubmitted = true;
            if (isValid) {
              
              diagramaService.ACrearDiagrama($scope.fDiagrama).then(function (object) {
                  var msg = object.data["msg"];
                  if (msg) flash(msg);
                  var label = object.data["label"];
                  $location.path(label);
                  $route.reload();
              });
            }
        };
        $scope.fDiagrama1Submitted = false;
        $scope.AModificarDiagrama1 = function(isValid) {
            $scope.fDiagrama1Submitted = true;
            if (isValid) {

                diagramaService.AModificarDiagrama($scope.fDiagrama1).then(function (object) {
                    var msg = object.data["msg"];
                    if (msg) flash(msg);
                    var label = object.data["label"];
                    $location.path(label);
                    $route.reload();
                });
            }
        };
        $scope.AEliminarDiagrama1 = function(idDiagrama) {
            diagramaService.AEliminarDiagrama({'idDiagrama':((typeof idDiagrama === 'object')?JSON.stringify(idDiagrama):idDiagrama)}).then(function (object) {
                var msg = object.data["msg"];
                if (msg) flash(msg);
                var label = object.data["label"];
                $location.path(label);
                $route.reload();
            });
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
        $scope.fEntidad1Submitted = false;
        $scope.AModificarEntidad1 = function(isValid) {
            $scope.fEntidad1Submitted = true;
            if (isValid) {

                entidadService.AModificarEntidad($scope.fEntidad1).then(function (object) {
                    var msg = object.data["msg"];
                    if (msg) flash(msg);
                    var label = object.data["label"];
                    $location.path(label);
                    $route.reload();
                });
            }
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
        $scope.VDiagrama1 = function(idDiagrama) {
            $location.path('/VDiagrama/'+((typeof idDiagrama === 'object')?JSON.stringify(idDiagrama):idDiagrama));
        };     
    }]
);