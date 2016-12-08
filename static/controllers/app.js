// Creación del módulo de la aplicación.
'use strict';

//Definimos una aplicacion de angular.
var mvcModule = angular.module('mvc', [
 'ngRoute',
 'flash',
 'ngTable'
]);

mvcModule.config(['$routeProvider',
    //Declaramos las rutas URL de la aplicación.
    function($routeProvider) {
        $routeProvider.
            when('/', {
                controller: 'VLoginController',
                templateUrl: 'static/views/identificar/VLogin.html',
            });
    }]
);

mvcModule.controller('mvcController', [
    '$scope', 
    '$http', 
    '$location',
    function($scope) {
        $scope.title = "Editor de Diagramas MVC";
    }]
);

mvcModule.directive('sameAs', [function () {
    return {
        restrict: 'A',
        scope:true,
        require: 'ngModel',
        link: function (scope, elem , attrs, control) {
            var checker = function () {
                //get the value of the this field
                var e1 = scope.$eval(attrs.ngModel); 
 
                //get the value of the other field
                var e2 = scope.$eval(attrs.sameAs);
                return e1 == e2;
            };
            scope.$watch(checker, function (n) {
 
                //set the form control to valid if both 
                //fields are the same, else invalid
                control.$setValidity("unique", n);
            });
        }
    };
}]);