mvcModule.config(function ($routeProvider) {
    $routeProvider.when('/VEntidad/:idEntidad', {
                controller: 'VEntidadController',
                templateUrl: 'static/views/entidad/VEntidad.html'
            });
});


// mvcModule.controller('VEntidadController', 
//    ['$scope', 
//     '$location', 
//     '$route', 
//     'flash', 
//     '$routeParams',
//     'entidadService',
//     'disenoService', 
//     'diagramaService',
//     'identificarService',
//     function ($scope, $location, $route, flash, $routeParams, entidadService, disenoService, diagramaService, identificarService) {
//         $scope.msg = '';
//         $scope.fEntidad = {};
//
//         entidadService.VEntidad({"idEntidad":$routeParams.idEntidad}).then(function (object) {
//             $scope.res = object.data;
//             for (var key in object.data) {
//                 $scope[key] = object.data[key];
//             }
//             if ($scope.logout) {
//                 $location.path('/');
//             }
//         });
//         $scope.VDiseno1 = function(idDiseno) {
//             $location.path('/VDiseno/'+idDiseno);
//         };
//         $scope.VLogin1 = function() {
//             $location.path('VLogin');
//         };
//     }]
// );