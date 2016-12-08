mvcModule.config(function ($routeProvider) {
    $routeProvider.when('/VLogin', {
                    controller: 'VLoginController',
                    templateUrl: 'static/views/identificar/VLogin.html'
                }).when('/VRegistro', {
                    controller: 'VRegistroController',
                    templateUrl: 'static/views/identificar/VRegistro.html'
                });
});

mvcModule.controller('VLoginController', [
    '$scope', 
    '$location', 
    '$route',
    'flash',
    'identificarService',
    function ($scope, $location, $route, flash, identificarService) {
        $scope.msg = '';
        $scope.fLogin = {};

        identificarService.VLogin().then(function (object) {
            $scope.res = object.data;
            for (var key in object.data) {
                $scope[key] = object.data[key];
            }
            if ($scope.logout) {
                $location.path('/');
            }
        });
        $scope.VRegistro1 = function() {
            $location.path('/VRegistro');
        };
        $scope.fLoginSumitted = false;
        $scope.AIdentificar1 = function(isValid) {
            $scope.fLoginSumitted = true;
            if (isValid) {
                identificarService.AIdentificar($scope.fLogin).then(
                    function (object) {
                        var msg = object.data['msg'];
                        if (msg) flash(msg);

                        var label = object.data['label'];
                        if (label == '/VLogin') {
                            $route.reload();
                        } else {
                            $location.path(label);
                        }
                    }
                );
            }
        };
    }]
);

mvcModule.controller('VRegistroController', [
    '$scope',
    '$location',
    '$route',
    'flash',
    'identificarService',
    function ($scope, $location, $route, flash, identificarService) {
        $scope.msg = '';
        $scope.fUsuario = {};

        identificarService.VRegistro().then(function (object) {
            $scope.res = object.data;
            for (var key in object.data) {
                $scope[key] = object.data[key];
            }
            if ($scope.logout) {
                $location.path('/');
            }
        });
        $scope.VLogin1 = function() {
            $location.path('/VLogin');
        };
        $scope.fUsuarioSumitted = false;
        $scope.ARegistrar1 = function(isValid) {
            $scope.fUsuarioSumitted = true;
            if (isValid) {
                identificarService.ARegistrar($scope.fUsuario).then(
                    function (object) {
                        var msg = object.data['msg'];
                        if (msg) flash(msg);

                        var label = object.data['label'];
                        if (label == "/VRegistro") {
                            $route.reload();
                        } else {
                            $location.path(label);
                        }
                    }
                );
            }
        };

    }]
);