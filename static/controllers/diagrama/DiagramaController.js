mvcModule.config(function ($routeProvider) {
    $routeProvider.when('/VDiagrama/:idDiagrama', {
                controller: 'VDiagramaController',
                templateUrl: 'static/views/diagrama/VDiagrama.html'
            });
});


mvcModule.controller('VDiagramaController', [
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
        $scope.tab = 1;
        $scope.seleccionado = 0;
        $scope.fDiagrama = {};
        $scope.fAccion = {};
        $scope.fAccion.relaciones_internas = [];
        $scope.fAccion.relaciones_externas = [];
        $scope.fElemento = {};
        $scope.fElemento.atributos = [];


        diagramaService.VDiagrama({"idDiagrama":$routeParams.idDiagrama}).then(function (object) {
            $scope.res = object.data;
            for (var key in object.data) {
                $scope[key] = object.data[key];
            }
            if ($scope.logout) {
                $location.path('/');
            }


    //-----------------------------------------------------------------------------
    //                               DIAGRAMA
    //-----------------------------------------------------------------------------

        // CONSTANTES
        const ANCHO_LETRA  = 9.5;          // Ancho que ocupa una letra.
        const ALTURA_LETRA = 20;          // Altura que ocupa una letra.
        const MARGEN_TEXTO = 13;          // Margen del texto interno de los nodos.
        const ANCHO_MIN_VISTA   = 12;     // Ancho minimo con el que se crean las vistas.
        const ALTURA_MIN_VISTA  = 4;      // Altura minima con el que se crean las vistas.
        const ANCHO_MIN_ACCION  = 80;     // Ancho minimo con el que se crean las acciones.
        const ALTURA_MIN_ACCION = 50;     // Altura maxima con el que se crean las acciones.
        const ANCHO_MIN_OP  = 80;         // Ancho minimo con el que se crean las operaciones.
        const ALTURA_MIN_OP = 30;         // Altura maxima con el que se crean las operaciones.
        const RADIO_MIN_EXTERNO = 50;     // Radio minimo con el que se crean los nodos externos.
        const CANT_LETRAS_POR_LINEA = 10; // Cantidad de letras por linea para los rombos, ovalos y circulos.
        const CANT_LINEAS_POR_ACCION = 3; 
        const CANT_LINEAS_POR_OPERACION = 3;
        const CANT_LINEAS_POR_EXTERNO = 3;
        const ALTURA_FLECHA = 16;           // Radio del circulo circunscrito en el triangulo de la flecha.



        // LECTURA DE DATOS
        // Interpretamos los datos que estan en formato json.
        var datos = JSON.stringify($scope.res.data5);
        var nodos = JSON.parse(datos);

        // Hacemos que origen y destino referencien al id de los nodos.
        nodos.enlaces.forEach(function(d) {
            var enlaces = d.visAcc||d.accVis||d.extVis||d.visExt||d.accExt||d.accOp||d.extAcc;
    
            for (var i = 0; i < enlaces.length; i++) {

                enlaces[i].origen = nodos.nodos[0].vistas.filter(function(n) { return n.id === enlaces[i].origen; })[0]      || 
                         nodos.nodos[1].acciones.filter(function(n) { return n.id === enlaces[i].origen; })[0]    || 
                         nodos.nodos[2].operaciones.filter(function(n) { return n.id === enlaces[i].origen; })[0] ||
                         nodos.nodos[3].externos.filter(function(n) { return n.id === enlaces[i].origen; })[0];

                enlaces[i].destino = nodos.nodos[0].vistas.filter(function(n) { return n.id === enlaces[i].destino; })[0]      || 
                          nodos.nodos[1].acciones.filter(function(n) { return n.id === enlaces[i].destino; })[0]    || 
                          nodos.nodos[2].operaciones.filter(function(n) { return n.id === enlaces[i].destino; })[0] ||
                          nodos.nodos[3].externos.filter(function(n) { return n.id === enlaces[i].destino; })[0];
            }
        });


        // CALCULOS REQUERIDOS.

        // Obtenemos el string mas largos de cada vista. Esto para calcular posteriormente 
        // el ancho de la misma.
        var textoMasLargo = {};

        nodos.nodos[0].vistas.forEach(function(d) {
            textoMasLargo[d.id] = obtenerTextoMasLargo(d.nombre, d.atributos);
        });


        // Calculamos el ancho y la altura de cada vista.
        nodos.nodos[0].vistas.forEach(function(d) {
            // Calculamos el ancho de la vista.
            var texto    = textoMasLargo[d.id];
            var tamTexto = texto.length;

            if (tamTexto < ANCHO_MIN_VISTA) {
                tamTexto = ANCHO_MIN_VISTA;
            }
            d.ancho = tamTexto*ANCHO_LETRA + 2*MARGEN_TEXTO;

            // Calculamos la altura de la vista.
            var cantAtributos = d.atributos.length+1;

            if (cantAtributos < ALTURA_MIN_VISTA) {
                cantAtributos = ALTURA_MIN_VISTA;
            }
			d.altura = cantAtributos*ALTURA_LETRA + 2*MARGEN_TEXTO;
        });


        // Calculamos el ancho y la altura de cada accion.
        nodos.nodos[1].acciones.forEach(function(d) {
            var tamNombre   = d.nombre.length;

            // Obtenemos la cantidad de lineas que ocupa el nombre.
            var cantlineas  = Math.floor(tamNombre/CANT_LETRAS_POR_LINEA);
            var restoLineas = tamNombre%CANT_LETRAS_POR_LINEA;
        
            var cant_letras_linea = CANT_LETRAS_POR_LINEA;

            if (cantlineas > CANT_LINEAS_POR_ACCION) {
                // Calculamos el excedente del maximo permitido.
                var exceso = Math.floor(cantlineas/CANT_LINEAS_POR_ACCION);
                var resto  = cantlineas%CANT_LINEAS_POR_ACCION;

                if (resto > 0) {
                    exceso += 1;
                }
                cant_letras_linea += 2*exceso; 
                cantlineas  = Math.floor(tamNombre/cant_letras_linea);
                restoLineas = tamNombre%cant_letras_linea;
            }     

            if (restoLineas > 0) {
                cantlineas += 1;
            }
                
            if (tamNombre > cant_letras_linea) {
                d.ancho  = 2*cant_letras_linea*ANCHO_LETRA;
                d.altura = 2*cantlineas*ALTURA_LETRA;
            } else {
                d.ancho  = 2*ANCHO_MIN_ACCION;
                d.altura = 2*ALTURA_MIN_ACCION;
            }
        });

        nodos.nodos[3].externos.forEach(function(d) {
            var tamNombre  = d.nombre.length;

            var cantlineas = Math.floor(tamNombre/CANT_LETRAS_POR_LINEA);
            var restoLineas = tamNombre%CANT_LETRAS_POR_LINEA;
            var radio; 

            var cant_letras_linea = CANT_LETRAS_POR_LINEA;

            if (cantlineas < CANT_LINEAS_POR_EXTERNO) {
                // Calculamos el excedente del maximo permitido.
                var exceso = Math.floor(cantlineas/CANT_LINEAS_POR_EXTERNO);
                var resto  = cantlineas%CANT_LINEAS_POR_EXTERNO;

                if (resto > 0) {
                    exceso += 1;
                }

                cant_letras_linea += 1.5*exceso;
                cantlineas = Math.floor(tamNombre/cant_letras_linea);
                restoLineas = tamNombre%cant_letras_linea;
            }

            if (restoLineas > 0) {
                cantlineas += 1;
            }

            if (tamNombre > cant_letras_linea) {
                d.radio = cant_letras_linea*ANCHO_LETRA/2;
            } else {
                d.radio = RADIO_MIN_EXTERNO;
            }
        });

        var info_acciones = obtenerPuertosAccion();
        var info_vistas   = obtenerPuertosLlegadaVista();
        var info_externos = obtenerPuertosExterno();

        // // Calculamos la cantidad de enlaces que recibe cada vista.
        // for (var i = 0; i < nodos.enlaces[1].accVis.length; i++) {
        //     enlaces_entrada_vista[nodos.enlaces[1].accVis[i].destino.id].cant += 1;
        // }
        // for (var i = 0; i < nodos.enlaces[3].extVis.length; i++) {
        //     enlaces_entrada_vista[nodos.enlaces[3].extVis[i].destino.id].cant +=1;
        // }

        // // Calculamos la cantidad de enlaces que recibe cada accion.
        // for (var i = 0; i < nodos.enlaces[0].visAcc.length; i++) {
        //     enlaces_entrada_accion[nodos.enlaces[0].visAcc[i].destino.id].cant += 1;
        // }
        // for (var i = 0; i < nodos.enlaces[5].extAcc.length; i++) {
        //     enlaces_entrada_accion[nodos.enlaces[5].extAcc[i].destino.id].cant +=1;
        // }

        // // Obtenemos las vistas y externos ordenados acorde a su posicion en y.
        // vistas_y_externos_ordenos = [];
        
        // vistas_y_externos_ordenos = valuesToArray(enlaces_entrada_vista);

        // vistas_y_externos_ordenos.sort(function(a, b) {
        //     if (a.y > b.y) {
        //         return 1;
        //     } 
        //     if (a.y < b.y) {
        //         return -1;
        //     }
        //     return 0;
        // });

        // // Obtenemos las acciones y externos ordenados acorde a su posicion en x.
        // acciones_y_externos_ordenos = [];
    
        // acciones_y_externos_ordenos = valuesToArray(enlaces_entrada_accion);

        // acciones_y_externos_ordenos.sort(function(a, b) {
        //     if (a.x > b.x) {
        //         return 1;
        //     } 
        //     if (a.x < b.x) {
        //         return -1;
        //     }
        //     return 0;
        // });

        // console.log("ordenados vista_externo");
        // console.log(vistas_y_externos_ordenos);
        // console.log("ordenados accion_externo");
        // console.log(acciones_y_externos_ordenos);


        // // Asignamos los puertos de llegada para las acciones.
        // for (var i = 0; i < acciones_y_externos_ordenos.length; i++) {
        //     console.log(acciones_y_externos_ordenos[i]);
        // }

        // console.log("Recorriendo los enaces");
        // Recorremos los enlaces para asignar los puertos. 
        // nodos.enlaces.forEach(function(d) {
        //     var enlaces = d.visAcc||d.extAcc;
          
        //     if (enlaces != undefined) {
          
        //         for (var j = 0; j < vistas_y_externos_ordenos.length; j++) {
        //             var nro_puerto = 0;
        //             for (var i = 0; i < enlaces.length; i++) {

        //                 if (vistas_y_externos_ordenos[j].id == enlaces[i].destino.id) {
        //                     enlaces[i]["puerto"] = (nro_puerto+=1);
        //                     // console.log(vistas_y_externos_ordenos[j],enlaces[i]);
        //                 }
        //             }
        //         }
        //     }
        // });







        // // Asignamos los numeros de puerto. 
        // enlaces_entrada_vista_ordenados.forEach(function(d) {
        //     var nro_puerto = 0;
        //     for (var i = 0; i < nodos.enlaces[1].accVis.length; i++) {
            
        //         if (nodos.enlaces[1].accVis[i].destino.id == d.id) {
        //             nro_puerto += 1;
        //             nodos.enlaces[1].accVis[i]["puerto"] = nro_puerto; 
        //         }
        //     }
        // });



            // // Asignamos los puertos de salidas y sus posiciones para cada atributo.
            // var nro_puerto = 0;
            // for (var i = 0; i < d.atributos.length; i++) {
            //     nro_puerto += 1;
            //     d.atributos[i]["puerto_salida"] = nro_puerto;

            //     // Posicion de salida del puerto en y.
            //     yOrig = d.y - d.altura/2 + 1.4*ALTURA_LETRA + (i+1)*ALTURA_LETRA;
            //     d.atributos[i]["y"] = yOrig;

            //     console.log(d.atributos[i]);
            // }

///////////////////////////////////////////////////////////////

                        // for (var j = 0; j < d.origen.atributos.length; j++) {
                        //     if (d.origen.atributos[j].id === id_salida) {
                        //         num = j;
                        //     }
                        // }

                        // // Posicion de salida del enlace en y.
                        // yOrig = d.origen.y - d.origen.altura/2 + 1.4*ALTURA_LETRA + (num+1)*ALTURA_LETRA; 
  
                        // var tamLineaHoriz;

                        // if (d.origen.y <= d.destino.y) {
                        //     tamLineaHoriz = 50*(d.origen.atributos.length-num);
                        // } else {
                        //     tamLineaHoriz = 50*(num+1);
                        // }

                        // // Obtenemos la cantidad de enlaces vista-accion.
                        // var cant_enlaces = nodos.enlaces[0].visAcc.length;
                        // var espaciado    = (d.destino.altura-MARGEN_TEXTO)/cant_enlaces;

                        // if (d.origen.x >= d.destino.x-d.destino.ancho && d.origen.x <= d.destino.x) {
                        //     xOrig = d.origen.x - d.origen.ancho/2;
                        //     xPto  = xOrig - tamLineaHoriz;
                        //     yDest = (d.destino.y-d.destino.altura/2-MARGEN_TEXTO)+(d.origen.atributos.length-num)*espaciado;
                        
                        // } else if (d.origen.x < d.destino.x+d.destino.ancho && d.origen.x > d.destino.x) {
                        //     xOrig = d.origen.x + d.origen.ancho/2;
                        //     xPto = xOrig + tamLineaHoriz;
                        //     yDest = (d.destino.y-d.destino.altura/2-MARGEN_TEXTO)+(d.origen.atributos.length-num)*espaciado;
                            
                        // } else if (d.origen.x < d.destino.x-d.destino.ancho) {
                        //     xOrig = d.origen.x + d.origen.ancho/2;
                        //     xPto  = xOrig + tamLineaHoriz;
                        //     yDest = (d.destino.y-d.destino.altura/2-MARGEN_TEXTO)+(num+1)*espaciado;

                        // } else {
                        //     xOrig = d.origen.x - d.origen.ancho/2;
                        //     xPto  = xOrig - tamLineaHoriz;  
                        //     yDest = (d.destino.y-d.destino.altura/2-MARGEN_TEXTO)+(num+1)*espaciado;                        
                        // }

                        // if (cant_enlaces == 1) { 
                        //     yDest = d.destino.y; 
                        // }
                        // //Guardamos la posicion donde parte el enlace.
                        // d.origen.atributos[num]["x1"]=xOrig;
                        // d.origen.atributos[num]["y1"]=yOrig;
                        // d.origen.atributos[num]["xPto"]=xPto;

///////////////////////////////////////////////////////////////









///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        // ATRIBUTOS SVG
        // Ancho y altura de la hoja del diagrama por defecto.
        var anchoSVG = 848;
        var altoSVG  = 800;
        var shiftKey;

        // Dependiendo de la cantidad de elementos definimos el tamano del svg.
        // Obtenemos la cantidad de nodos por tipo y seleccionamos el mayor para obtener el alto.
        // var cantNodosPorTipo = [];
        // cantNodosPorTipo[0] = $scope.res.data5.nodos[0].vistas.length;
        // cantNodosPorTipo[1] = $scope.res.data5.nodos[1].acciones.length;
        // cantNodosPorTipo[2] = $scope.res.data5.nodos[2].operaciones.length;
        // cantNodosPorTipo[3] = $scope.res.data5.nodos[3].externos.length;

        // var maximo = 0;
        // for (var n = 0; n < $scope.res.data5.nodos.length; n++) {
        //     if (maximo <= cantNodosPorTipo[n]) {
        //         maximo = cantNodosPorTipo[n];
        //     }
        // }

        //FALTA COMPLETAR LO DEL TAMANO DE LA HOJA



        //Creamos la hoja donde se muestra el diagrama.
        var svg = d3.select("#dibujo")
                    .append("svg")
                    .attr("width", anchoSVG)
                    .attr("height", altoSVG)
                    .selectAll("g");

        //Permite realizar definiciones para reusar elementos.
        var defs = svg
                    .data([""]).enter()
                    .append("defs");

        
        //ENLACES AGRUPADOS.
        //Enlaces dirigidos de vista-accion agrupados.
        var relacionVA = svg
                    .data(nodos.enlaces[0].visAcc).enter()
                    .append("g")
                    .attr("id", function(d,i) {return "va"+i;});

        //Enlaces dirigidos de accion-vista agrupados.
        var relacionAV = svg
                    .data(nodos.enlaces[1].accVis).enter()
                    .append("g")
                    .attr("id", function(d,i) {return "av"+i;});
      
        //Enlaces dirigidos de vista-accion agrupados.
        var relacionVE = svg
                    .data(nodos.enlaces[2].visExt).enter()
                    .append("g")
                    .attr("id", function(d,i) {return "ve"+i;});

        //Enlaces dirigidos de accion-vista agrupados.
        var relacionEV = svg
                    .data(nodos.enlaces[3].extVis).enter()
                    .append("g")
                    .attr("id", function(d,i) {return "ev"+i;});

        //Enlaces dirigidos de accion-externo agrupados.
        var relacionAE = svg
                    .data(nodos.enlaces[4].accExt).enter()
                    .append("g")
                    .attr("id", function(d,i) {return "ae"+i;});

        //Enlaces dirigidos de externo-accion agrupados.
        var relacionEA = svg
                    .data(nodos.enlaces[5].extAcc).enter()
                    .append("g")
                    .attr("id", function(d,i) {return "ea"+i;});

        //Enlaces no dirigidos de accion-operacion agrupados.
        var relacionAO = svg
                    .data(nodos.enlaces[6].accOp).enter()
                    .append("g")
                    .attr("id", function(d,i) {return "ao"+i;});

        
        //NODOS AGRUPADOS
        //Nodos de tipo vista agrupados.
        var vista = svg
                    .data(nodos.nodos[0].vistas).enter()
                    .append("g")
                    .attr("class", "nodo")
                    .attr("id", function(d,i) {return "v"+i;})
                    .attr("transform", function(d) {
                        return "translate("+d.x+","+d.y+")";
                    })
                    .on("click", function(d) {
                        $scope.seleccionado = 1;
                        $scope.fVista = {"idNodo": d.id, "nombre": d.nombre, 
                                         "atributos": d.atributos,
                                         "nombre_atributo": "",
                                         "atributos_eliminar": []};


                        console.log(d);

                        // Seleccionamos el tab 2 (Elemento) usando JQuery.
                        $('#myTab li a').eq(0).trigger('click');
                    })
                    .on("mousedown", function(d) {
                        d.selected = true;
                    })
                    .on("mouseup", function(d) {
                        diagramaService.AGuardarPosicionDiagrama(d);

                        d.selected = false;
                        if (d.selected && shiftKey)
                            d3.select(this).classed("seleccionado", d.selected = false);
                    })
                    .call(d3.behavior.drag()
                        .on("drag", function(d) { 
                            mover(d3.event.dx, d3.event.dy); 
                        })
                    );

        //Nodos de tipo accion agrupados.
        var accion = svg
                    .data(nodos.nodos[1].acciones).enter()
                    .append("g")
                    .attr("class", "nodo")
                    .attr("id", function(d,i) {return "a"+i;})
                    .attr("transform", function(d) {
                        return "translate("+d.x+","+d.y+")";
                    })
                    .on("click", function(d) {
                        $scope.seleccionado = 2;
                        $scope.fAccion = {"idNodo": d.id, 
                                          "nombre": d.nombre, 
                                          "vista_interna": d.vista_interna, 
                                          "vista_externa": d.vista_externa,
                                          "relaciones_internas": d.relaciones_internas,
                                          "relaciones_externas": d.relaciones_externas,
                                          "rela_internas_eliminar": [],
                                          "rela_externas_eliminar": []};

                        // Seleccionamos el tab 2 (Elemento) usando JQuery.
                        $('#myTab li a').eq(0).trigger('click');
                    })
                    .on("mousedown", function(d) {
                        d.selected = true;
                    })
                    .on("mouseup", function(d) {
                        diagramaService.AGuardarPosicionDiagrama(d);

                        d.selected = false;

                       })
                    .call(d3.behavior.drag()
                        .on("drag", function(d) { 
                            mover(d3.event.dx, d3.event.dy); 
                        })
                    );

        //Nodos de tipo operacion agrupados.
        var operacion = svg
                    .data(nodos.nodos[2].operaciones).enter()
                    .append("g")
                    .attr("class", "nodo")
                    .attr("id", function(d,i) {return "o"+i;})
                    .attr("transform", function(d) {
                        return "translate("+d.x+","+d.y+")";
                    })
                    .on("click", function(d) {
                        $scope.seleccionado = 3;
                        $scope.fOperacion = {"idNodo": d.id, 
                                             "nombre": d.nombre, 
                                             "idEntidad": d.idEntidad, 
                                             "idAccion": d.idAccion};

                        // Seleccionamos el tab 2 (Elemento) usando JQuery.
                        $('#myTab li a').eq(0).trigger('click');
                    })
                    .on("mousedown", function(d) {
                        d.selected = true;
                    })
                    .on("mouseup", function(d) {
                        diagramaService.AGuardarPosicionDiagrama(d);

                        d.selected = false;
                    })
                    .call(d3.behavior.drag()
                        .on("drag", function(d) { 
                            mover(d3.event.dx, d3.event.dy); 
                        })
                    );

        //Nodos de tipo externo agrupados.
        var externo = svg
                    .data(nodos.nodos[3].externos).enter()
                    .append("g")
                    .attr("class", "nodo")
                    .attr("id", function(d,i) {return "e"+i;})
                    .attr("transform", function(d) {
                        return "translate("+d.x+","+d.y+")";
                    })
                    .on("click", function(d) {
                        $scope.seleccionado = 4;
                    })
                    .on("mousedown", function(d) {
                        d.selected = true;
                    })
                    .on("mouseup", function(d) {
                        diagramaService.AGuardarPosicionDiagrama(d);

                        d.selected = false;
                    })
                    .call(d3.behavior.drag()
                        .on("drag", function(d) { 
                            mover(d3.event.dx, d3.event.dy); 
                        })
                    );

        var circulosV = svg
                    .data(nodos.nodos[0].vistas).enter()
                    .append("g")
                    .attr("class", "nodo");

        // var circulosR = svg
        //             .data(nodos.nodos[1].acciones).enter()
        //             .append("g")
        //             .attr("class", "nodo");


        var circulosRIzq = svg
                    .data(nodos.nodos[1].acciones).enter()
                    .append("g")
                    .attr("class", "nodo");

        var circulosRDer = svg
                    .data(nodos.nodos[1].acciones).enter()
                    .append("g")
                    .attr("class", "nodo");


        // var circulosO = svg
        //             .data(nodos.nodos[2].operaciones).enter()
        //             .append("g")
        //             .attr("class", "nodo");

        // var circulosE = svg
        //             .data(nodos.nodos[3].externos).enter()
        //             .append("g")
        //             .attr("class", "nodo");

        // DIBUJANDO LOS VISTAS.
        var rectV = vista
                .append("rect")
                .attr("x", function(d) { 
                    // Obtenemos el texto mas largo de la vista actual.
                    var texto    = textoMasLargo[d.id];
                    var tamTexto = texto.length;

                    if (tamTexto < ANCHO_MIN_VISTA) {
                       tamTexto = ANCHO_MIN_VISTA;
                    }
                    return -tamTexto*ANCHO_LETRA/2 - MARGEN_TEXTO;
                })
                .attr("y", function(d) {
                    // Obtenemos la cantidad de atributos de la vista incluyendo el nombre.
                    var cantAtributos = d.atributos.length+1;

                    if (cantAtributos < ALTURA_MIN_VISTA) {
                        cantAtributos = ALTURA_MIN_VISTA;
                    }
                    return -cantAtributos*ALTURA_LETRA/2 - MARGEN_TEXTO;
                }) 
                .attr("rx", 20) // Borde redondeado.
                .attr("ry", 20) // Borde redondeado.
                .attr("width", function(d) { return d.ancho; })
                .attr("height", function(d) { return d.altura; });

        // Nombre de la vista.
        var nombreV = vista
                    .append("text")
                    .text(function(d) {return d.nombre;})
                    .attr("x", 0)
                    .attr("y", function(d) {
                        // Obtenemos la cantidad de atributos de la vista incluyendo el nombre.
                        var cantAtributos = d.atributos.length+1;

                        if (cantAtributos < ALTURA_MIN_VISTA) {
                            cantAtributos = ALTURA_MIN_VISTA;
                        }
                        return -cantAtributos*ALTURA_LETRA/2;
                    })
                    .attr("text-anchor", "middle")
                    .attr("dy", ALTURA_LETRA/2);

        // Linea bajo el nombre de la vista.
        var lineaV = vista
                .append("line")
                .attr("x1", function(d) { return -d.ancho/2; })
                .attr("y1", function(d) { return -d.altura/2 + 1.6*ALTURA_LETRA; })
                .attr("x2", function(d) { return d.ancho/2; })
                .attr("y2", function(d) { return -d.altura/2 + 1.6*ALTURA_LETRA; });

        // Nombres de los atributos de la vista.
        var atributosV = vista
                .each(function(d, i) {
                    var items = d3.select(this)
                        .selectAll("g")
                        .data(d.atributos).enter()
                        .append("text")
                        .text(function(e) {return e.nombre;})
                        .attr("x", function(e,i) {
                            // Obtenemos el texto mas largo de la vista actual.
                            var texto    = textoMasLargo[d.id];
                            var tamTexto = texto.length;

                            if (tamTexto < ANCHO_MIN_VISTA) {
                                tamTexto = ANCHO_MIN_VISTA;
                            }
                            return -tamTexto*ANCHO_LETRA/2;
                        })
                        .attr("y", function(e,i) { return -d.altura/2 + 1.6*ALTURA_LETRA + (i+1)*ALTURA_LETRA; })
                        .attr("text-anchor", "start");
                });



        // DIBUJANDO LAS ACCIONES.
        var romboA = accion
                .append("polygon")
                .attr("points", function(d) {
                    var ancho  = d.ancho;
                    var altura = d.altura;

                    puntos = (ancho/2)+" "+0+", "+0+" "+(altura/2)+", "+(-ancho/2)+" "+0+", "+0+" "+(-altura/2);

                    return puntos;
                });

        // Nombre de la accion.
        var nombreA = accion
                .append("g")
                .each(function(d,i){
                    var tamNombre   = d.nombre.length; 

                    // Obtenemos la cantidad de lineas que ocupa el nombre.
                    var cantlineas  = Math.floor(tamNombre/CANT_LETRAS_POR_LINEA);
                    var restoLineas = tamNombre%CANT_LETRAS_POR_LINEA;

                    var arregloText = [];
                    var cant_letras_linea = CANT_LETRAS_POR_LINEA;

                    if (cantlineas > CANT_LINEAS_POR_ACCION) {
                        // Calculamos el excedente del maximo permitido.
                        var exceso = Math.floor(cantlineas/CANT_LINEAS_POR_ACCION);
                        var resto  = cantlineas%CANT_LINEAS_POR_ACCION;

                        if (resto > 0) {
                            exceso += 1;
                        }

                        cant_letras_linea += 2*exceso; 
                        cantlineas  = Math.floor(tamNombre/cant_letras_linea);
                        restoLineas = tamNombre%cant_letras_linea;
                    }

                    if (restoLineas > 0) {
                        cantlineas += 1;
                    }

                    if (tamNombre > cant_letras_linea) {

                        for (var i = 0; i < cantlineas; i++) {
                            var tmp = d.nombre.slice(i*cant_letras_linea, (i+1)*cant_letras_linea);
                            arregloText.push(tmp);
                        }
                    } else {
                        arregloText.push(d.nombre);
                    }

                    var lineas = d3.select(this)
                        .selectAll("text")
                        .data(arregloText).enter()
                        .append("text")
                        .text(function(d) {return d;})
                        .attr("x", 0)
                        .attr("y", function(d, i) {
                            return -cantlineas*ALTURA_LETRA/2 + MARGEN_TEXTO + i*ALTURA_LETRA;
                        })
                        .attr("text-anchor", "middle");
                });



        // DIBUJANDO LOS NODOS OPERACION.
        var ovaloO = operacion
                    .append("ellipse")
                    .attr("cx", 0)
                    .attr("cy", 0)
                    .attr("rx", function(d) {
                        var tamNombre  = d.nombre.length;

                        // Obtenemos la cantidad de lineas que ocupa el nombre.
                        var cantlineas = Math.floor(tamNombre/CANT_LETRAS_POR_LINEA);
                        var restoLineas = tamNombre%CANT_LETRAS_POR_LINEA;
                        var ancho; 

                        var cant_letras_linea = CANT_LETRAS_POR_LINEA;

                        if (cantlineas > CANT_LINEAS_POR_OPERACION) {
                            // Calculamos el excedente del maximo permitido.
                            var exceso = Math.floor(cantlineas/CANT_LINEAS_POR_OPERACION);
                            var resto  = cantlineas%CANT_LINEAS_POR_OPERACION;

                            if (resto > 0) {
                                exceso += 1;
                            }

                            cant_letras_linea += 1.5*exceso; 
                            cantlineas  = Math.floor(tamNombre/cant_letras_linea);
                            restoLineas = tamNombre%cant_letras_linea;
                        }

                        if (restoLineas > 0) {
                            cantlineas += 1;
                        }

                        if (tamNombre > cant_letras_linea) {
                            ancho = cant_letras_linea*ANCHO_LETRA; 
                        } else {
                            ancho = ANCHO_MIN_OP;
                        }
                        return ancho;
                    })
                    .attr("ry", function(d) {
                        var tamNombre  = d.nombre.length;

                        // Obtenemos la cantidad de lineas que ocupa el nombre.
                        var cantlineas = Math.floor(tamNombre/CANT_LETRAS_POR_LINEA);
                        var restoLineas = tamNombre%CANT_LETRAS_POR_LINEA;
                        var altura; 

                        var cant_letras_linea = CANT_LETRAS_POR_LINEA;

                        if (cantlineas > CANT_LINEAS_POR_OPERACION) {
                            // Calculamos el excedente del maximo permitido.
                            var exceso = Math.floor(cantlineas/CANT_LINEAS_POR_OPERACION);
                            var resto  = cantlineas%CANT_LINEAS_POR_OPERACION;

                            if (resto > 0) {
                                exceso += 1;
                            }

                            cant_letras_linea += 2*exceso; 
                            cantlineas  = Math.floor(tamNombre/cant_letras_linea);
                            restoLineas = tamNombre%cant_letras_linea;
                        }

                        if (restoLineas > 0) {
                            cantlineas += 1;
                        }

                        if (tamNombre > cant_letras_linea) {
                            altura = cantlineas*ALTURA_LETRA-MARGEN_TEXTO;
                        } else {
                            altura = ALTURA_MIN_OP;
                        }
                        return altura; 
                    });


        //Nombre de las operaciones.
        var nombreO = operacion
                .append("g")
                .each(function(d,i){
                    var tamNombre   = d.nombre.length; 

                    // Obtenemos la cantidad de lineas que ocupa el nombre.
                    var cantlineas  = Math.floor(tamNombre/CANT_LETRAS_POR_LINEA);
                    var restoLineas = tamNombre%CANT_LETRAS_POR_LINEA;

                    var arregloText = [];
                    var cant_letras_linea = CANT_LETRAS_POR_LINEA;

                    if (cantlineas > CANT_LINEAS_POR_OPERACION) {
                        // Calculamos el excedente del maximo permitido.
                        var exceso = Math.floor(cantlineas/CANT_LINEAS_POR_OPERACION);
                        var resto  = cantlineas%CANT_LINEAS_POR_OPERACION;

                        if (resto > 0) {
                            exceso += 1;
                        }

                        cant_letras_linea += 2*exceso; 
                        cantlineas  = Math.floor(tamNombre/cant_letras_linea);
                        restoLineas = tamNombre%cant_letras_linea;
                    }

                    if (restoLineas > 0) {
                        cantlineas += 1;
                    }

                    if (tamNombre > cant_letras_linea) {

                        for (var i = 0; i < cantlineas; i++) {
                            var tmp = d.nombre.slice(i*cant_letras_linea, (i+1)*cant_letras_linea);
                            arregloText.push(tmp);
                        }
                    } else {
                        arregloText.push(d.nombre);
                    }

                    var lineas = d3.select(this)
                        .selectAll("text")
                        .data(arregloText).enter()
                        .append("text")
                        .text(function(d) {return d;})
                        .attr("x", 0)
                        .attr("y", function(d, i) {
                            return -cantlineas*ALTURA_LETRA/2 + MARGEN_TEXTO + i*ALTURA_LETRA;
                        })
                        .attr("text-anchor", "middle");
                });

        //DIBUJANDO LOS NODOS EXTERNOS.
        var circuloE = externo
                    .append("circle")
                    .attr("r", function(d) { return d.radio; })
                    .attr("cx", 0)
                    .attr("cy", 0);

        //Nombre del nodo externo.
        var nombreE = externo
              .append("g")
              .each(function(d,i){
                    var tamNombre   = d.nombre.length; 

                    // Obtenemos la cantidad de lineas que ocupa el nombre.
                    var cantlineas  = Math.floor(tamNombre/CANT_LETRAS_POR_LINEA);
                    var restoLineas = tamNombre%CANT_LETRAS_POR_LINEA;

                    var arregloText = [];
                    var cant_letras_linea = CANT_LETRAS_POR_LINEA;

                    if (cantlineas > CANT_LINEAS_POR_EXTERNO) {
                        // Calculamos el excedente del maximo permitido.
                        var exceso = Math.floor(cantlineas/CANT_LINEAS_POR_EXTERNO);
                        var resto  = cantlineas%CANT_LINEAS_POR_EXTERNO;

                        if (resto > 0) {
                            exceso += 1;
                        }

                        cant_letras_linea += 2*exceso; 
                        cantlineas  = Math.floor(tamNombre/cant_letras_linea);
                        restoLineas = tamNombre%cant_letras_linea;
                    }

                    if (restoLineas > 0) {
                        cantlineas += 1;
                    }

                    if (tamNombre > cant_letras_linea) {

                        for (var i = 0; i < cantlineas; i++) {
                            var tmp = d.nombre.slice(i*cant_letras_linea, (i+1)*cant_letras_linea);
                            arregloText.push(tmp);
                        }
                    } else {
                        arregloText.push(d.nombre);
                    }

                  var lineas = d3.select(this)
                      .selectAll("text")
                      .data(arregloText).enter()
                      .append("text")
                      .text(function(d) {return d;})
                      .attr("x", 0)
                      .attr("y", function(d, i) {
                          return -cantlineas*ALTURA_LETRA/2 + MARGEN_TEXTO + i*ALTURA_LETRA;
                      })
                      .attr("text-anchor", "middle");
              });



                // var posV = circulosV
                //     .append('circle')
                //     .attr("r", 3)
                //     .attr("cx", function(d) {return d.x;})
                //     .attr("cy", function(d) {return d.y;});

                // var posR = circulosR
                //     .append('circle')
                //     .attr("r", 3)
                //     .attr("cx", function(d) {return d.x;})
                //     .attr("cy", function(d) {return d.y;});

                // var posR = circulosRIzq
                //     .append('circle')
                //     .attr("r", 3)
                //     .attr("cx", function(d) {return d.x - d.ancho/2;})
                //     .attr("cy", function(d) {return d.y;});

                // var posR = circulosRDer
                //     .append('circle')
                //     .attr("r", 3)
                //     .attr("cx", function(d) {return d.x + d.ancho/2;})
                //     .attr("cy", function(d) {return d.y;});

                // var posO = circulosO
                //     .append('circle')
                //     .attr("r", 3)
                //     .attr("cx", function(d) {return d.x;})
                //     .attr("cy", function(d) {return d.y;});

                // var posE = circulosE
                //     .append('circle')
                //     .attr("r", 3)
                //     .attr("cx", function(d) {return d.x;})
                //     .attr("cy", function(d) {return d.y;});


        //DIBUJANDO LOS ENLACES.

        // Enlaces dirigidos de tipo vista-accion.
        var enlaceVA = relacionVA
                    .append("path")
                    .attr("class", "enlaceVA")
                    .attr("d", function(d, i) {
                        var id_salida = d.id_salida;

                        for (var j = 0; j < d.origen.atributos.length; j++) {
                            if (d.origen.atributos[j].id === id_salida) {
                                num = j;
                            }
                        }

                        // Obtenemos el puerto asignado a este enlace.
                        var acciones = [];
                        var esta_a_la_izq = true;

                        if (d.origen.x <= d.destino.x) {
                            acciones = info_acciones[d.destino.id].rela_izq;
                        } else {
                            esta_a_la_izq = false;
                            acciones = info_acciones[d.destino.id].rela_der;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < acciones.length; k++) {
                            if (acciones[k].id == d.origen.id && acciones[k].id_salida == id_salida) {
                                nro_puerto = acciones[k].puerto;
                            }
                        }

                        // Posicion de salida del enlace en y.
                        yOrig = d.origen.y - d.origen.altura/2 + 1.4*ALTURA_LETRA + (num+1)*ALTURA_LETRA; 

                        var tamLineaHoriz;

                        if (d.origen.y <= d.destino.y) {
                         tamLineaHoriz = 50*(d.origen.atributos.length-num);
                        } else {
                         tamLineaHoriz = 50*(num+1);
                        }

                        var cant_enlaces = acciones.length;
                        var espaciado    = (d.destino.altura-MARGEN_TEXTO)/cant_enlaces;
                        var posInicio    = d.destino.y-d.destino.altura/2+MARGEN_TEXTO/2;

                        if (d.origen.x >= d.destino.x-d.destino.ancho && d.origen.x <= d.destino.x) {
                            xOrig = d.origen.x - d.origen.ancho/2;
                            xPto  = xOrig - tamLineaHoriz;
                        
                        } else if (d.origen.x < d.destino.x+d.destino.ancho && d.origen.x > d.destino.x) {
                            xOrig = d.origen.x + d.origen.ancho/2;
                            xPto = xOrig + tamLineaHoriz;
                            
                        } else if (d.origen.x < d.destino.x-d.destino.ancho) {
                            xOrig = d.origen.x + d.origen.ancho/2;
                            xPto  = xOrig + tamLineaHoriz;

                        } else {
                            xOrig = d.origen.x - d.origen.ancho/2;
                            xPto  = xOrig - tamLineaHoriz;                        
                        }

                        yDest = posInicio+nro_puerto*espaciado; 

                        if (cant_enlaces == 1) { 
                            yDest = d.destino.y; 
                        }

                        // console.log("nombre",d.origen.nombre,"salida",id_salida,"puerto",nro_puerto, "altura", d.destino.altura, nro_puerto*espaciado);
                        //Guardamos la posicion donde parte el enlace.
                        d.origen.atributos[num]["x1"]=xOrig;
                        d.origen.atributos[num]["y1"]=yOrig;
                        d.origen.atributos[num]["xPto"]=xPto;
                        
                        xDest = d.destino.x;

                        linea = "M"+xOrig+","+yOrig+
                                " L"+xPto+","+yOrig+
                                " L"+xPto+","+yDest+
                                " L"+xDest+","+yDest;

                        //Guardamos la posicion donde llega el enlace.
                        d.origen.atributos[num]["x2"]=xDest;
                        d.origen.atributos[num]["y2"]=yDest;

                        return linea;
                    });

        // Triangulo de la flecha para las relaciones vista-accion.
        var flechaA = relacionVA
                    .append("polygon")
                    .attr("class", "flechaA")
                    .attr("points", function(d) {
                    	var id_salida = d.id_salida;
                    	var num;

                        for (var j = 0; j < d.origen.atributos.length; j++) {
                            if (d.origen.atributos[j].id === id_salida) {
                                num = j;
                            }
                        }

                        var xDest;
                        var yDest = d.origen.atributos[num].y2;
                        // Obtenemos el valor de x en base al y anterior.

                        if (yDest == d.destino.y) {

                            if (d.origen.x <= d.destino.x) {
                                xDest = d.destino.x - d.destino.ancho/2;
                            } else {
                                xDest = d.destino.x + d.destino.ancho/2;
                            }
                        } else {
                            xDest = obtenerPosicionFlecha(yDest, d.origen.x, d.destino.x, d.destino.y, d.destino.ancho, d.destino.altura);
                    	}

                    	if (d.origen.x <= d.destino.x) {
                    		puntos = xDest+","+yDest+" "+(xDest-ALTURA_FLECHA)+","+(yDest+ALTURA_FLECHA/3)+" "+(xDest-ALTURA_FLECHA)+","+(yDest-ALTURA_FLECHA/3);                   	
                    	} else {
                    		puntos = xDest+","+yDest+" "+(xDest+ALTURA_FLECHA)+","+(yDest+ALTURA_FLECHA/3)+" "+(xDest+ALTURA_FLECHA)+","+(yDest-ALTURA_FLECHA/3);
                    	}
                    	return puntos;
                    });


        // Enlaces dirigidos de tipo accion-vista.
        var enlaceAV  = relacionAV
                    .append("path")
                    .attr("class", "enlaceAV")
                    .attr("d", function(d, i) { 
                        //  Obtenemos el puerto asignado en la vista para este enlace.
                        var acciones = [];
                        
                        // Buscamos el puerto asignado en la accion.
                        if (d.destino.x <= d.origen.x) {
                            acciones = info_acciones[d.origen.id].rela_izq;
                        } else {
                            acciones = info_acciones[d.origen.id].rela_der;
                        }

                        cant_enlaces = acciones.length;
                        espaciado_accion = (d.destino.altura-MARGEN_TEXTO)/cant_enlaces;
                        posInicio    = d.origen.y-d.origen.altura/2+MARGEN_TEXTO/2;

                        var nro_puerto = 0;
                        for (var k = 0; k < acciones.length; k++) {
                            if (acciones[k].id == d.destino.id) {
                                nro_puerto = acciones[k].puerto;
                            }
                        }   

                        //  Posicion de salida en y desde a accion.
                        yOrig = posInicio+nro_puerto*espaciado_accion;
                        xOrig = d.origen.x;

                        if (cant_enlaces == 1) {
                            yOrig = d.origen.y
                        } 

                        var tamLineaHoriz;

                        if (d.origen.x <= d.destino.x) {
                            tamLineaHoriz = 50*(acciones.length-i);
                        } else {
                            tamLineaHoriz = -50*(acciones.length-i);
                        }
                    
                        // Buscamos el puerto asignado en la vista.
                        vistas = [];
                        if (d.origen.y <= d.destino.y) {
                            vistas = info_vistas[d.destino.id].rela_abajo;
                        } else {
                            vistas = info_vistas[d.destino.id].rela_arriba;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < vistas.length; k++) {
                            if (vistas[k].id == d.origen.id) {
                                nro_puerto = vistas[k].puerto;
                            }
                        }   

                        var cant_enlaces    = vistas.length;
                        var espaciado_vista = (d.destino.ancho-2*MARGEN_TEXTO)/cant_enlaces;
                        var posInicio       = d.destino.x - d.destino.ancho/2 - MARGEN_TEXTO;

                        if (d.origen.y >= d.destino.y - d.destino.altura &&  d.origen.y <= d.destino.y) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else if (d.origen.y <= d.destino.y + d.destino.altura && d.origen.y > d.destino.y) {
                            yDest = d.destino.y + d.destino.altura/2;
                        } else if (d.origen.y < d.destino.y - d.destino.altura) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else {
                            yDest = d.destino.y + d.destino.altura/2;
                        }

                        xDest = posInicio+nro_puerto*espaciado_vista;

                        if (cant_enlaces == 1) { 
                            xDest = d.destino.x; 
                        }

                        // console.log("nombre",d.origen.nombre,"salida",id_salida,"puerto",nro_puerto, "altura", d.destino.altura, nro_puerto*espaciado);
                        //Guardamos la posicion donde parte el enlace.
                        d["x1"]=xOrig;
                        d["y1"]=yOrig;
                        
                        xDest = d.destino.x;

                        linea = "M"+xOrig+","+yOrig+
                                " L"+xDest+","+yOrig+
                                " L"+xDest+","+yDest;

                        //Guardamos la posicion donde llega el enlace.
                        d["x2"]=xDest;
                        d["y2"]=yDest;

                        return linea;
                    });

       	// Triangulo de la flecha para las relaciones accion-vista.
        var flechaV1 = relacionAV
                    .append("polygon")
                    .attr("class", "flechaV")
                    .attr("points", function(d) {
                        var yDest, xDest;

                        // Buscamos el puerto asignado en la vista.
                        vistas = [];
                        if (d.origen.y <= d.destino.y) {
                            vistas = info_vistas[d.destino.id].rela_abajo;
                        } else {
                            vistas = info_vistas[d.destino.id].rela_arriba;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < vistas.length; k++) {
                            if (vistas[k].id == d.origen.id) {
                                nro_puerto = vistas[k].puerto;
                            }
                        }   

                        var cant_enlaces    = vistas.length;
                        var espaciado_vista = (d.destino.ancho-2*MARGEN_TEXTO)/cant_enlaces;
                        var posInicio       = d.destino.x - d.destino.ancho/2 + MARGEN_TEXTO;

                        if (d.origen.y >= d.destino.y - d.destino.altura &&  d.origen.y <= d.destino.y) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else if (d.origen.y <= d.destino.y + d.destino.altura && d.origen.y > d.destino.y) {
                            yDest = d.destino.y + d.destino.altura/2;
                        } else if (d.origen.y < d.destino.y - d.destino.altura) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else {
                            yDest = d.destino.y + d.destino.altura/2;
                        }

                        xDest = posInicio+nro_puerto*espaciado_vista;

                        if (cant_enlaces == 1) { 
                            xDest = d.destino.x; 
                        }
                    	
                    	if (d.origen.y <= d.destino.y) {
                    		puntos = xDest+","+yDest+" "+(xDest-ALTURA_FLECHA/3)+","+(yDest-ALTURA_FLECHA)+" "+(xDest+ALTURA_FLECHA/3)+","+(yDest-ALTURA_FLECHA);                   	
                    	} else {
                    		puntos = xDest+","+yDest+" "+(xDest-ALTURA_FLECHA/3)+","+(yDest+ALTURA_FLECHA)+" "+(xDest+ALTURA_FLECHA/3)+","+(yDest+ALTURA_FLECHA);
                    	}
                    	return puntos;
                    });

        // Enlaces dirigidos de tipo vista-externo.
        var enlaceVE = relacionVE
                    .append("line")
                    .attr("class", "enlaceVE")
                    .attr("x1", function(d) { return d.origen.x; })
                    .attr("y1", function(d) { return d.origen.y; })
                    .attr("x2", function(d) { return d.destino.x; })
                    .attr("y2", function(d) { return d.destino.y; });

        // Enlaces dirigidos de tipo vista-externo.
        var enlaceEV = relacionEV
                    .append("path")
                    .attr("class", "enlaceEV")
                    .attr("d", function(d, i) { 
                        var externos = [];
                        
                        // Buscamos el puerto asignado en el externo.
                        if (d.destino.x <= d.origen.x) {
                            externos = info_externos[d.origen.id].rela_izq;
                        } else {
                            externos = info_externos[d.origen.id].rela_der;
                        }

                        cant_enlaces = externos.length;
                        espaciado_externo = (d.origen.radio-MARGEN_TEXTO)/cant_enlaces;
                        posInicio    = d.origen.y-d.origen.radio+MARGEN_TEXTO/2;

                        var nro_puerto = 0;
                        for (var k = 0; k < externos.length; k++) {
                            if (externos[k].id == d.destino.id) {
                                nro_puerto = externos[k].puerto;
                            }
                        }   

                        //  Posicion de salida en y desde a accion.
                        yOrig = posInicio+nro_puerto*espaciado_externo;
                        xOrig = d.origen.x;

                        if (cant_enlaces == 1) {
                            yOrig = d.origen.y
                        } 

                        var tamLineaHoriz;

                        if (d.origen.x <= d.destino.x) {
                            tamLineaHoriz = 50*(externos.length-i);
                        } else {
                            tamLineaHoriz = -50*(externos.length-i);
                        }
                    
                        // Buscamos el puerto asignado en la vista.
                        vistas = [];
                        if (d.origen.y <= d.destino.y) {
                            vistas = info_vistas[d.destino.id].rela_abajo;
                        } else {
                            vistas = info_vistas[d.destino.id].rela_arriba;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < vistas.length; k++) {
                            if (vistas[k].id == d.origen.id) {
                                nro_puerto = vistas[k].puerto;
                            }
                        }   

                        var cant_enlaces    = vistas.length;
                        var espaciado_vista = (d.destino.ancho-2*MARGEN_TEXTO)/cant_enlaces;
                        var posInicio       = d.destino.x - d.destino.ancho/2 + MARGEN_TEXTO;

                        if (d.origen.y >= d.destino.y - d.destino.altura &&  d.origen.y <= d.destino.y) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else if (d.origen.y <= d.destino.y + d.destino.altura && d.origen.y > d.destino.y) {
                            yDest = d.destino.y + d.destino.altura/2;
                        } else if (d.origen.y < d.destino.y - d.destino.altura) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else {
                            yDest = d.destino.y + d.destino.altura/2;
                        }

                        xDest = posInicio+nro_puerto*espaciado_vista;

                        if (cant_enlaces == 1) { 
                            xDest = d.destino.x; 
                        }

                        //Guardamos la posicion donde parte el enlace.
                        d["x1"]=xOrig;
                        d["y1"]=yOrig;
                        
                        xDest = d.destino.x;

                        linea = "M"+xOrig+","+yOrig+
                                " L"+xDest+","+yOrig+
                                " L"+xDest+","+yDest;

                        //Guardamos la posicion donde llega el enlace.
                        d["x2"]=xDest;
                        d["y2"]=yDest;

                        return linea;
                    });

        // Triangulo de la flecha para las relaciones externo-vista.
        var flechaV2 = relacionEV
                    .append("polygon")
                    .attr("class", "flechaV")
                    .attr("points", function(d) {
                        var yDest, xDest;

                        // Buscamos el puerto asignado en la vista.
                        vistas = [];
                        if (d.origen.y <= d.destino.y) {
                            vistas = info_vistas[d.destino.id].rela_abajo;
                        } else {
                            vistas = info_vistas[d.destino.id].rela_arriba;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < vistas.length; k++) {
                            if (vistas[k].id == d.origen.id) {
                                nro_puerto = vistas[k].puerto;
                            }
                        }   

                        var cant_enlaces    = vistas.length;
                        var espaciado_vista = (d.destino.ancho-2*MARGEN_TEXTO)/cant_enlaces;
                        var posInicio       = d.destino.x - d.destino.ancho/2 + MARGEN_TEXTO;

                        if (d.origen.y >= d.destino.y - d.destino.altura &&  d.origen.y <= d.destino.y) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else if (d.origen.y <= d.destino.y + d.destino.altura && d.origen.y > d.destino.y) {
                            yDest = d.destino.y + d.destino.altura/2;
                        } else if (d.origen.y < d.destino.y - d.destino.altura) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else {
                            yDest = d.destino.y + d.destino.altura/2;
                        }

                        xDest = posInicio+nro_puerto*espaciado_vista;

                        if (cant_enlaces == 1) { 
                            xDest = d.destino.x; 
                        }
                        
                        if (d.origen.y <= d.destino.y) {
                            puntos = xDest+","+yDest+" "+(xDest-ALTURA_FLECHA/3)+","+(yDest-ALTURA_FLECHA)+" "+(xDest+ALTURA_FLECHA/3)+","+(yDest-ALTURA_FLECHA);                       
                        } else {
                            puntos = xDest+","+yDest+" "+(xDest-ALTURA_FLECHA/3)+","+(yDest+ALTURA_FLECHA)+" "+(xDest+ALTURA_FLECHA/3)+","+(yDest+ALTURA_FLECHA);
                        }
                        return puntos;
                    });


        // Enlaces dirigidos de tipo accion-externo.
        var enlaceAE = relacionAE
                    .append("line")
                    .attr("class", "enlaceAE")
                    .attr("x1", function(d) { return d.origen.x; })
                    .attr("y1", function(d) { return d.origen.y; })
                    .attr("x2", function(d) { return d.destino.x; })
                    .attr("y2", function(d) { return d.destino.y; });

        var enlaceEA = relacionEA
                    .append("path")
                    .attr("class", "enlaceEA")
                    .attr("d", function(d, i) {
                        var id_salida = d.id_salida;
                        // Obtenemos el puerto asignado a este enlace.
                        var acciones = [];

                        if (d.origen.x <= d.destino.x) {
                            acciones = info_acciones[d.destino.id].rela_izq;
                        } else {
                            esta_a_la_izq = false;
                            acciones = info_acciones[d.destino.id].rela_der;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < acciones.length; k++) {
                            if (acciones[k].id == d.origen.id && acciones[k].id_salida == id_salida) {
                                nro_puerto = acciones[k].puerto;
                            }
                        }

                        // Posicion de salida del enlace en y.
                        yOrig = d.origen.y; 
                        xOrig = d.origen.x;

                        var tamLineaHoriz;

                        if (d.origen.y <= d.destino.y) {
                            tamLineaHoriz = 50*(acciones.length-i);
                        } else {
                            tamLineaHoriz = -50*(acciones.length-i);
                        }

                        var cant_enlaces = acciones.length;
                        var espaciado    = (d.destino.altura-MARGEN_TEXTO)/cant_enlaces;
                        var posInicio    = d.destino.y-d.destino.altura/2+MARGEN_TEXTO/2;

                        xPto  = xOrig + tamLineaHoriz;
                        yDest = posInicio+nro_puerto*espaciado; 

                        if (cant_enlaces == 1) { 
                            yDest = d.destino.y; 
                        }

                        // console.log("nombre",d.origen.nombre,"salida",id_salida,"puerto",nro_puerto, "altura", d.destino.altura, nro_puerto*espaciado);
                        //Guardamos la posicion donde parte el enlace.
                        d["x1"]=xOrig;
                        d["y1"]=yOrig;
                        d["xPto"]=xPto;
                        
                        xDest = d.destino.x;

                        linea = "M"+xOrig+","+yOrig+
                                " L"+xPto+","+yOrig+
                                " L"+xPto+","+yDest+
                                " L"+xDest+","+yDest;

                        //Guardamos la posicion donde llega el enlace.
                        d["x2"]=xDest;
                        d["y2"]=yDest;

                        return linea;
                    });
                    // .append("line")
                    // .attr("class", "enlaceEA")
                    // .attr("x1", function(d) { return d.origen.x; })
                    // .attr("y1", function(d) { return d.origen.y; })
                    // .attr("x2", function(d) { return d.destino.x; })
                    // .attr("y2", function(d) { return d.destino.y; });

        // Enlaces no dirigidos de tipo accion-operacion.
        var enlaceAO = relacionAO
                    .append("line")
                    .attr("class", "enlaceAO")
                    .attr("x1", function(d) { return d.origen.x; })
                    .attr("y1", function(d) { return d.origen.y; })
                    .attr("x2", function(d) { return d.destino.x; })
                    .attr("y2", function(d) { return d.destino.y; });



        // FUNCIONES AUXILIARES

        // Funcion para obtener el texto mas largo de los componentes de una vista.
        function obtenerTextoMasLargo(nombre, atributos){

            var max = nombre.length;
            var textoMasLargo = nombre;

            for (var i = 0; i < atributos.length; i++) {
                if (atributos[i].nombre.length > max) {
                max = atributos[i].nombre.length;
                textoMasLargo = atributos[i].nombre;
            }
        }
        return textoMasLargo;
        }

        //Función que permite obtener el desplazamiento en x de la flecha que apunta a una acción.
        function obtenerPosicionFlecha(pto, xOrig, xDestRombo, yDestRombo, anchoRombo, alturaRombo) {
        	var pendiente;
        	var punto;

        	if (xOrig <= xDestRombo && pto < yDestRombo) {
	        	pendiente = -anchoRombo/alturaRombo;
	        	punto = pendiente*(pto-yDestRombo+alturaRombo/2)+xDestRombo;

	        } else if (xOrig <= xDestRombo && pto > yDestRombo) {
	        	pendiente = anchoRombo/alturaRombo;
	        	punto = pendiente*(pto-yDestRombo-alturaRombo/2)+xDestRombo;

	        } else if (xOrig > xDestRombo && pto < yDestRombo) {
	        	pendiente = anchoRombo/alturaRombo;
	        	punto = pendiente*(pto-yDestRombo)+xDestRombo+ anchoRombo/2;

	        } else {
	        	pendiente = -anchoRombo/alturaRombo;
	        	punto = pendiente*(pto-yDestRombo)+xDestRombo+ anchoRombo/2;
	        }
        	return punto;
        }


        function obtenerPuertosLlegadaVista() {
            // Obtenemos las entradas de las vistas.
            var vistas = {};

            nodos.enlaces.forEach(function(d) {

                if (d.accVis != undefined) {
                    for (var j = 0; j < d.accVis.length; j++) {

                        var id_vista = d.accVis[j].destino.id;

                        if (vistas[id_vista] == undefined) {
                            vistas[id_vista] = {"x":d.accVis[j].destino.x, "y":d.accVis[j].destino.y, "rela_arriba":[], "rela_abajo":[]};
                            vistas[id_vista]["relaciones"] = [{"id":d.accVis[j].origen.id, "x":d.accVis[j].origen.x, "y":d.accVis[j].origen.y}]
                        } else {
                            vistas[id_vista].relaciones.push({"id":d.accVis[j].origen.id, "x":d.accVis[j].origen.x, "y":d.accVis[j].origen.y});
                        }
                    }
                } else if (d.extVis != undefined) {
                    for (var j = 0; j < d.extVis.length; j++) {

                        var id_vista = d.extVis[j].destino.id;

                        if (vistas[id_vista] == undefined) {
                            vistas[id_vista] = {"x":d.extVis[j].destino.x, "y":d.extVis[j].destino.y, "rela_arriba":[], "rela_abajo":[]};
                            vistas[id_vista]["relaciones"] = [{"id":d.extVis[j].origen.id, "x":d.extVis[j].origen.x, "y":d.extVis[j].origen.y}]
                        } else {
                            vistas[id_vista].relaciones.push({"id":d.extVis[j].origen.id, "x":d.extVis[j].origen.x, "y":d.extVis[j].origen.y});
                        }
                    }
                }

            });
            var idVistas = Object.keys(vistas);

            // Ordenamos las salidas para asignarle los puertos.
            for (var k = 0; k < idVistas.length; k++) {
                vistas[idVistas[k]].relaciones.sort(function(a, b) {
                    if (a.x > b.x) {
                        return 1;
                    } 
                    if (a.x < b.x) {
                        return -1;
                    }
                    return 0;
                });
            }

            // Una vez ordenados separamos los que estan arriba y abajo.
            var nro_puerto_arriba = 0;
            var nro_puerto_abajo  = 0;
            for (k = 0; k < idVistas.length; k++) {
                for (var c = 0; c < vistas[idVistas[k]].relaciones.length; c++) {

                    if (vistas[idVistas[k]].relaciones[c].y <= vistas[idVistas[k]].y) {
                        nro_puerto_abajo += 1;
                        vistas[idVistas[k]].relaciones[c]["puerto"] = nro_puerto_abajo;
                        vistas[idVistas[k]].rela_abajo.push(vistas[idVistas[k]].relaciones[c]);
                    } else {
                        nro_puerto_arriba += 1;
                        vistas[idVistas[k]].relaciones[c]["puerto"] = nro_puerto_arriba;
                        vistas[idVistas[k]].rela_arriba.push(vistas[idVistas[k]].relaciones[c]);
                    }
                }
            }
            console.log("XXXXXXXXXXXXXX Vistas XXXXXXXXXXXXXXXXXXXXx");
            console.log(vistas);
            console.log("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx");
            return vistas;
        }

        function obtenerPuertosExterno() {
            // Obtenemos las entradas y las salidas de los nodos externos.
            var externos = {};

            nodos.enlaces.forEach(function(d) {

                if (d.accExt != undefined) {
                    for (var j = 0; j < d.accExt.length; j++) {

                        var id_externo = d.accExt[j].destino.id;

                        if (externos[id_externo] == undefined) {
                            externos[id_externo] = {"x":d.accExt[j].destino.x, "y":d.accExt[j].destino.y, "rela_izq":[], "rela_der":[]};                 
                            externos[id_externo]["relaciones"] = [{"id":d.accExt[j].origen.id, "x":d.accExt[j].origen.x, "y":d.accExt[j].origen.y}];
                        } else {
                            acciones[id_accion].relaciones.push({"id":d.accExt[j].origen.id, "x":d.accExt[j].origen.x, "y":d.accExt[j].origen.y});
                        }
                    }

                } else if (d.extAcc != undefined) {
                    for (var j = 0; j < d.extAcc.length; j++) {

                        var id_externo = d.extAcc[j].origen.id;

                        if (externos[id_externo] == undefined) {
                            externos[id_externo] = {"x":d.extAcc[j].origen.x, "y":d.extAcc[j].origen.y, "rela_izq":[], "rela_der":[]};
                            externos[id_externo]["relaciones"] = [{"id":d.extAcc[j].destino.id, "x":d.extAcc[j].destino.x, "y":d.extAcc[j].destino.y}]
                        } else {
                            externos[id_externo].relaciones.push({"id":d.extAcc[j].destino.id, "x":d.extAcc[j].destino.x, "y":d.extAcc[j].destino.y});
                        }
                    }

                } else if (d.visExt != undefined) {
                    for (var j = 0; j < d.visExt.length; j++) {

                        var id_externo = d.visExt[j].destino.id;

                        if (externos[id_externo] == undefined) {
                            externos[id_externo] = {"x":d.visExt[j].destino.x, "y":d.visExt[j].destino.y, "rela_izq":[], "rela_der":[]};                 
                            externos[id_externo]["relaciones"] = [{"id":d.visExt[j].origen.id, "x":d.visExt[j].origen.x, "y":d.visExt[j].origen.y, "id_salida": d.visExt[j].id_salida}];
                        } else {
                            externos[id_externo].relaciones.push({"id":d.visExt[j].origen.id, "x":d.visExt[j].origen.x, "y":d.visExt[j].origen.y, "id_salida": d.visExt[j].id_salida});
                        }
                    }

                } else if (d.extVis != undefined) {
                    for (var j = 0; j < d.extVis.length; j++) {

                        var id_externo = d.extVis[j].origen.id;

                        if (externos[id_externo] == undefined) {
                            externos[id_externo] = {"x":d.extVis[j].origen.x, "y":d.extVis[j].origen.y, "rela_izq":[], "rela_der":[]};
                            externos[id_externo]["relaciones"] = [{"id":d.extVis[j].destino.id, "x":d.extVis[j].destino.x, "y":d.extVis[j].destino.y}];
                        } else {
                            externos[id_externo].relaciones.push({"id":d.extVis[j].destino.id, "x":d.extVis[j].destino.x, "y":d.extVis[j].destino.y});
                        }
                    } 
                }
            });

            // Ordenamos las que tengan id salida.
            var idExternos = Object.keys(externos);

            for (var k = 0; k < idExternos.length; k++) {
                externos[idExternos[k]].relaciones.sort(function(a, b) {
                       
                    if (a.id_salida != undefined && b.id_salida != undefined) { 
                        if (a.id_salida > b.id_salida) {
                            return 1;
                        }    
                        if (a.id_salida < b.id_salida) {
                            return -1;
                        }
                    }
                    return 0;
                });
            }

            // Ordenamos las entradas y salidas para asignarle los puertos.
            for (var k = 0; k < idExternos.length; k++) {
                externos[idExternos[k]].relaciones.sort(function(a, b) {
                    if (a.y > b.y) {
                        return 1;
                    } 
                    if (a.y < b.y) {
                        return -1;
                    }
                    return 0;
                });
            }

            // Una vez ordenados separamos los que estan a la izquierda de los que estan a la derecha.
            var nro_puerto_izq = 0;
            var nro_puerto_der = 0;
            for (k = 0; k < idExternos.length; k++) {
                for (var c = 0; c < externos[idExternos[k]].relaciones.length; c++) {

                    if (externos[idExternos[k]].relaciones[c].x <= externos[idExternos[k]].x) {
                        nro_puerto_izq += 1;
                        externos[idExternos[k]].relaciones[c]["puerto"] = nro_puerto_izq;
                        externos[idExternos[k]].rela_izq.push(externos[idExternos[k]].relaciones[c]);
                    } else {
                        nro_puerto_der += 1;
                        externos[idExternos[k]].relaciones[c]["puerto"] = nro_puerto_der;
                        externos[idExternos[k]].rela_der.push(externos[idExternos[k]].relaciones[c]);
                    }
                }
            }
            console.log("XXXXXXXXXXXXXXX Externos XXXXXXXXXXXXXXXXXXXx");
            console.log(externos);
            console.log("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx");
            return externos;
        }

        function obtenerPuertosAccion() {
            // Obtenemos las entradas y salidas de las acciones.
            var acciones = {};
            nodos.enlaces.forEach(function(d) {

                if (d.visAcc != undefined) {
                    for (var j = 0; j < d.visAcc.length; j++) {

                        var id_accion = d.visAcc[j].destino.id;

                        if (acciones[id_accion] == undefined) {
                            acciones[id_accion] = {"x":d.visAcc[j].destino.x, "y":d.visAcc[j].destino.y, "rela_izq":[], "rela_der":[]};                 
                            acciones[id_accion]["relaciones"] = [{"id":d.visAcc[j].origen.id, "x":d.visAcc[j].origen.x, "y":d.visAcc[j].origen.y, "id_salida": d.visAcc[j].id_salida}];
                        } else {
                            acciones[id_accion].relaciones.push({"id":d.visAcc[j].origen.id, "x":d.visAcc[j].origen.x, "y":d.visAcc[j].origen.y, "id_salida": d.visAcc[j].id_salida});
                        }
                    }
                } else if (d.extAcc != undefined) {
                    for (var j = 0; j < d.extAcc.length; j++) {

                        var id_accion = d.extAcc[j].destino.id;

                        if (acciones[id_accion] == undefined) {
                            acciones[id_accion] = {"x":d.extAcc[j].destino.x, "y":d.extAcc[j].destino.y, "rela_izq":[], "rela_der":[]};
                            acciones[id_accion]["relaciones"] = [{"id":d.extAcc[j].origen.id, "x":d.extAcc[j].origen.x, "y":d.extAcc[j].origen.y}];
                        } else {
                            acciones[id_accion].relaciones.push({"id":d.extAcc[j].origen.id, "x":d.extAcc[j].origen.x, "y":d.extAcc[j].origen.y});
                        }
                    }  
                } else if (d.accVis != undefined) {
                    for (var j = 0; j < d.accVis.length; j++) {

                        var id_accion = d.accVis[j].origen.id;

                        if (acciones[id_accion] == undefined) {
                            acciones[id_accion] = {"x":d.accVis[j].origen.x, "y":d.accVis[j].origen.y, "rela_izq":[], "rela_der":[]};
                            acciones[id_accion]["relaciones"] = [{"id":d.accVis[j].destino.id, "x":d.accVis[j].destino.x, "y":d.accVis[j].destino.y}];
                        } else {
                            acciones[id_accion].relaciones.push({"id":d.accVis[j].destino.id, "x":d.accVis[j].destino.x, "y":d.accVis[j].destino.y});
                        }
                    }  
                } else if (d.accExt != undefined) {
                    for (var j = 0; j < d.accExt.length; j++) {

                        var id_accion = d.accExt[j].origen.id;

                        if (acciones[id_accion] == undefined) {
                            acciones[id_accion] = {"x":d.accExt[j].origen.x, "y":d.accExt[j].origen.y, "rela_izq":[], "rela_der":[]};
                            acciones[id_accion]["relaciones"] = [{"id":d.accExt[j].destino.id, "x":d.accExt[j].destino.x, "y":d.accExt[j].destino.y}];
                        } else {
                            acciones[id_accion].relaciones.push({"id":d.accExt[j].destino.id, "x":d.accExt[j].destino.x, "y":d.accExt[j].destino.y});
                        }
                    }     
                }
            });

            // Ordenamos las que tengan id salida.
            var idAcciones = Object.keys(acciones);

            for (var k = 0; k < idAcciones.length; k++) {
                acciones[idAcciones[k]].relaciones.sort(function(a, b) {
                       
                    if (a.id_salida != undefined && b.id_salida != undefined) { 
                        if (a.id_salida > b.id_salida) {
                            return 1;
                        }    
                        if (a.id_salida < b.id_salida) {
                            return -1;
                        }
                    }
                    return 0;
                });
            }

            // Ordenamos las entradas y salidas para asignarle los puertos.
            for (var k = 0; k < idAcciones.length; k++) {
                acciones[idAcciones[k]].relaciones.sort(function(a, b) {
                    if (a.y > b.y) {
                        return 1;
                    } 
                    if (a.y < b.y) {
                        return -1;
                    }
                    return 0;
                });
            }

            // Una vez ordenados separamos los que estan a la izquierda de los que estan a la erecha.
            var nro_puerto_izq = 0;
            var nro_puerto_der = 0;
            for (k = 0; k < idAcciones.length; k++) {
                for (var c = 0; c < acciones[idAcciones[k]].relaciones.length; c++) {

                    if (acciones[idAcciones[k]].relaciones[c].x <= acciones[idAcciones[k]].x) {
                        nro_puerto_izq += 1;
                        acciones[idAcciones[k]].relaciones[c]["puerto"] = nro_puerto_izq;
                        acciones[idAcciones[k]].rela_izq.push(acciones[idAcciones[k]].relaciones[c]);
                    } else {
                        nro_puerto_der += 1;
                        acciones[idAcciones[k]].relaciones[c]["puerto"] = nro_puerto_der;
                        acciones[idAcciones[k]].rela_der.push(acciones[idAcciones[k]].relaciones[c]);
                    }
                }
            }
            console.log("XXXXXXXXXXXXXXX Acciones XXXXXXXXXXXXXXXXXXXx");
            console.log(acciones);
            console.log("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx");
            return acciones;
        }


        //Funcion que permite desplazar los elementos.
        function mover(dx, dy) {

        vista.filter(function(d) {return d.selected;})
            .attr("transform", function(d) {
                return "translate("+(d.x+=dx)+","+(d.y+=dy)+")";
            });
        info_vistas   = obtenerPuertosLlegadaVista();
            
        accion.filter(function(d) {return d.selected;})
            .attr("transform", function(d) {
                return "translate("+(d.x+=dx)+","+(d.y+=dy)+")";
            });
        info_acciones = obtenerPuertosAccion();

        operacion.filter(function(d) {return d.selected;})
            .attr("transform", function(d) {
                return "translate("+(d.x+=dx)+","+(d.y+=dy)+")";
            });

        externo.filter(function(d) {return d.selected;})
            .attr("transform", function(d) {
                return "translate("+(d.x+=dx)+","+(d.y+=dy)+")";
            });
        info_externos = obtenerPuertosExterno();

        enlaceVA.filter(function(d) {return d.origen.selected;})
                    .attr("d", function(d, i) {
                        var id_salida = d.id_salida;

                        for (var j = 0; j < d.origen.atributos.length; j++) {
                            if (d.origen.atributos[j].id === id_salida) {
                                num = j;
                            }
                        }

                        // Obtenemos el puerto asignado a este enlace.
                        var acciones = [];
                        var esta_a_la_izq = true;

                        if (d.origen.x <= d.destino.x) {
                            acciones = info_acciones[d.destino.id].rela_izq;
                        } else {
                            esta_a_la_izq = false;
                            acciones = info_acciones[d.destino.id].rela_der;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < acciones.length; k++) {
                            if (acciones[k].id == d.origen.id && acciones[k].id_salida == id_salida) {
                                nro_puerto = acciones[k].puerto;
                            }
                        }

                        // Posicion de salida del enlace en y.
                        yOrig = d.origen.y - d.origen.altura/2 + 1.4*ALTURA_LETRA + (num+1)*ALTURA_LETRA; 

                        var tamLineaHoriz;

                        if (d.origen.y <= d.destino.y) {
                         tamLineaHoriz = 50*(d.origen.atributos.length-num);
                        } else {
                         tamLineaHoriz = 50*(num+1);
                        }

                        var cant_enlaces;
                        var espaciado;
                        var posInicio;
                        
                        if (esta_a_la_izq) {
                            // Obtenemos la cantidad de enlaces vista-accion que llegan a la accion.
                            cant_enlaces = info_acciones[d.destino.id].rela_izq.length;
                            espaciado    = (d.destino.altura-MARGEN_TEXTO)/cant_enlaces;
                            posInicio    = d.destino.y-d.destino.altura/2-MARGEN_TEXTO/2;

                        } else {
                            // Obtenemos la cantidad de enlaces vista-accion que llegan a la accion.
                            cant_enlaces = info_acciones[d.destino.id].rela_der.length;
                            espaciado    = (d.destino.altura-MARGEN_TEXTO)/cant_enlaces;
                            posInicio    = d.destino.y-d.destino.altura/2-MARGEN_TEXTO/2;
                        }

                        if (d.origen.x >= d.destino.x-d.destino.ancho && d.origen.x <= d.destino.x) {
                            xOrig = d.origen.x - d.origen.ancho/2;
                            xPto  = xOrig - tamLineaHoriz;
                        
                        } else if (d.origen.x < d.destino.x+d.destino.ancho && d.origen.x > d.destino.x) {
                            xOrig = d.origen.x + d.origen.ancho/2;
                            xPto = xOrig + tamLineaHoriz;
                            
                        } else if (d.origen.x < d.destino.x-d.destino.ancho) {
                            xOrig = d.origen.x + d.origen.ancho/2;
                            xPto  = xOrig + tamLineaHoriz;

                        } else {
                            xOrig = d.origen.x - d.origen.ancho/2;
                            xPto  = xOrig - tamLineaHoriz;                        
                        }

                        yDest = posInicio+nro_puerto*espaciado; 

                        if (cant_enlaces == 1) { 
                            yDest = d.destino.y; 
                        }

                        //Guardamos la posicion donde parte el enlace.
                        d.origen.atributos[num]["x1"]=xOrig;
                        d.origen.atributos[num]["y1"]=yOrig;
                        d.origen.atributos[num]["xPto"]=xPto;
                        
                        xDest = d.destino.x;

                        linea = "M"+xOrig+","+yOrig+
                                " L"+xPto+","+yOrig+
                                " L"+xPto+","+yDest+
                                " L"+xDest+","+yDest;

                        //Guardamos la posicion donde llega el enlace.
                        d.origen.atributos[num]["x2"]=xDest;
                        d.origen.atributos[num]["y2"]=yDest;

                        return linea;
                    });

        enlaceVA.filter(function(d) {return d.destino.selected;})
                    .attr("d", function(d, i) {
                        var id_salida = d.id_salida;

                        for (var j = 0; j < d.origen.atributos.length; j++) {
                            if (d.origen.atributos[j].id === id_salida) {
                                num = j;
                            }
                        }

                        // Obtenemos el puerto asignado a este enlace.
                        var acciones = [];
                        var esta_a_la_izq = true;

                        if (d.origen.x <= d.destino.x) {
                            acciones = info_acciones[d.destino.id].rela_izq;
                        } else {
                            esta_a_la_izq = false;
                            acciones = info_acciones[d.destino.id].rela_der;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < acciones.length; k++) {
                            if (acciones[k].id == d.origen.id && acciones[k].id_salida == id_salida) {
                                nro_puerto = acciones[k].puerto;
                            }
                        }

                        // Posicion de salida del enlace en y.
                        yOrig = d.origen.y - d.origen.altura/2 + 1.4*ALTURA_LETRA + (num+1)*ALTURA_LETRA; 

                        var tamLineaHoriz;

                        if (d.origen.y <= d.destino.y) {
                         tamLineaHoriz = 50*(d.origen.atributos.length-num);
                        } else {
                         tamLineaHoriz = 50*(num+1);
                        }

                        var cant_enlaces;
                        var espaciado;
                        var posInicio;
                        
                        if (esta_a_la_izq) {
                            // Obtenemos la cantidad de enlaces vista-accion que llegan a la accion.
                            cant_enlaces = info_acciones[d.destino.id].rela_izq.length;
                            espaciado    = (d.destino.altura-MARGEN_TEXTO)/cant_enlaces;
                            posInicio    = d.destino.y-d.destino.altura/2-MARGEN_TEXTO/2;

                        } else {
                            // Obtenemos la cantidad de enlaces vista-accion que llegan a la accion.
                            cant_enlaces = info_acciones[d.destino.id].rela_der.length;
                            espaciado    = (d.destino.altura-MARGEN_TEXTO)/cant_enlaces;
                            posInicio    = d.destino.y-d.destino.altura/2-MARGEN_TEXTO/2;
                        }

                        if (d.origen.x >= d.destino.x-d.destino.ancho && d.origen.x <= d.destino.x) {
                            xOrig = d.origen.x - d.origen.ancho/2;
                            xPto  = xOrig - tamLineaHoriz;
                        
                        } else if (d.origen.x < d.destino.x+d.destino.ancho && d.origen.x > d.destino.x) {
                            xOrig = d.origen.x + d.origen.ancho/2;
                            xPto = xOrig + tamLineaHoriz;
                            
                        } else if (d.origen.x < d.destino.x-d.destino.ancho) {
                            xOrig = d.origen.x + d.origen.ancho/2;
                            xPto  = xOrig + tamLineaHoriz;

                        } else {
                            xOrig = d.origen.x - d.origen.ancho/2;
                            xPto  = xOrig - tamLineaHoriz;                        
                        }

                        yDest = posInicio+nro_puerto*espaciado; 

                        if (cant_enlaces == 1) { 
                            yDest = d.destino.y; 
                        }

                        //Guardamos la posicion donde parte el enlace.
                        d.origen.atributos[num]["x1"]=xOrig;
                        d.origen.atributos[num]["y1"]=yOrig;
                        d.origen.atributos[num]["xPto"]=xPto;
                        
                        xDest = d.destino.x;

                        linea = "M"+xOrig+","+yOrig+
                                " L"+xPto+","+yOrig+
                                " L"+xPto+","+yDest+
                                " L"+xDest+","+yDest;

                        //Guardamos la posicion donde llega el enlace.
                        d.origen.atributos[num]["x2"]=xDest;
                        d.origen.atributos[num]["y2"]=yDest;

                        return linea;
                    });

        flechaA.attr("points", function(d) {
                        var id_salida = d.id_salida;
                        var num;

                        for (var j = 0; j < d.origen.atributos.length; j++) {
                            if (d.origen.atributos[j].id === id_salida) {
                                num = j;
                            }
                        }

                        var xDest;
                        var yDest = d.origen.atributos[num].y2;
                        // Obtenemos el valor de x en base al y anterior.

                        if (yDest == d.destino.y) {

                            if (d.origen.x <= d.destino.x) {
                                xDest = d.destino.x - d.destino.ancho/2;
                            } else {
                                xDest = d.destino.x + d.destino.ancho/2;
                            }
                        } else {
                            xDest = obtenerPosicionFlecha(yDest, d.origen.x, d.destino.x, d.destino.y, d.destino.ancho, d.destino.altura);
                        }

                        if (d.origen.x <= d.destino.x) {
                            puntos = xDest+","+yDest+" "+(xDest-ALTURA_FLECHA)+","+(yDest+ALTURA_FLECHA/3)+" "+(xDest-ALTURA_FLECHA)+","+(yDest-ALTURA_FLECHA/3);                       
                        } else {
                            puntos = xDest+","+yDest+" "+(xDest+ALTURA_FLECHA)+","+(yDest+ALTURA_FLECHA/3)+" "+(xDest+ALTURA_FLECHA)+","+(yDest-ALTURA_FLECHA/3);
                        }
                        return puntos;
                    });

        enlaceAV.filter(function(d) {return d.origen.selected;})
                    .attr("d", function(d, i) { 
                        //  Obtenemos el puerto asignado en la vista para este enlace.
                        var acciones = [];
                        
                        // Buscamos el puerto asignado en la accion.
                        if (d.destino.x <= d.origen.x) {
                            acciones = info_acciones[d.origen.id].rela_izq;
                        } else {
                            acciones = info_acciones[d.origen.id].rela_der;
                        }

                        cant_enlaces = acciones.length;
                        espaciado_accion = (d.destino.altura-MARGEN_TEXTO)/cant_enlaces;
                        posInicio    = d.origen.y-d.origen.altura/2-MARGEN_TEXTO/2;

                        var nro_puerto = 0;
                        for (var k = 0; k < acciones.length; k++) {
                            if (acciones[k].id == d.destino.id) {
                                nro_puerto = acciones[k].puerto;
                            }
                        }   

                        //  Posicion de salida en y desde a accion.
                        yOrig = posInicio+nro_puerto*espaciado_accion;
                        xOrig = d.origen.x;

                        if (cant_enlaces == 1) {
                            yOrig = d.origen.y
                        } 

                        var tamLineaHoriz;

                        if (d.origen.x <= d.destino.x) {
                            tamLineaHoriz = 50*(acciones.length-i);
                        } else {
                            tamLineaHoriz = -50*(acciones.length-i);
                        }
                    
                        // Buscamos el puerto asignado en la vista.
                        vistas = [];
                        if (d.origen.y <= d.destino.y) {
                            vistas = info_vistas[d.destino.id].rela_abajo;
                        } else {
                            vistas = info_vistas[d.destino.id].rela_arriba;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < vistas.length; k++) {
                            if (vistas[k].id == d.origen.id) {
                                nro_puerto = vistas[k].puerto;
                            }
                        }   

                        var cant_enlaces    = vistas.length;
                        var espaciado_vista = (d.destino.ancho-2*MARGEN_TEXTO)/cant_enlaces;
                        var posInicio       = d.destino.x - d.destino.ancho/2 - MARGEN_TEXTO;


                        if (d.origen.y >= d.destino.y - d.destino.altura &&  d.origen.y <= d.destino.y) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else if (d.origen.y <= d.destino.y + d.destino.altura && d.origen.y > d.destino.y) {
                            yDest = d.destino.y + d.destino.altura/2;
                        } else if (d.origen.y < d.destino.y - d.destino.altura) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else {
                            yDest = d.destino.y + d.destino.altura/2;
                        }

                        xDest = posInicio+nro_puerto*espaciado_vista;

                        if (cant_enlaces == 1) { 
                            xDest = d.destino.x; 
                        }

                        // console.log("nombre",d.origen.nombre,"salida",id_salida,"puerto",nro_puerto, "altura", d.destino.altura, nro_puerto*espaciado);
                        //Guardamos la posicion donde parte el enlace.
                        d["x1"]=xOrig;
                        d["y1"]=yOrig;
                        
                        xDest = d.destino.x;

                        linea = "M"+xOrig+","+yOrig+
                                " L"+xDest+","+yOrig+
                                " L"+xDest+","+yDest;

                        //Guardamos la posicion donde llega el enlace.
                        d["x2"]=xDest;
                        d["y2"]=yDest;

                        return linea;
        });

        enlaceAV.filter(function(d) {return d.destino.selected;})
                    .attr("d", function(d, i) { 
                        //  Obtenemos el puerto asignado en la vista para este enlace.
                        var acciones = [];
                        
                        // Buscamos el puerto asignado en la accion.
                        if (d.destino.x <= d.origen.x) {
                            acciones = info_acciones[d.origen.id].rela_izq;
                        } else {
                            acciones = info_acciones[d.origen.id].rela_der;
                        }

                        cant_enlaces = acciones.length;
                        espaciado_accion = (d.destino.altura-MARGEN_TEXTO)/cant_enlaces;
                        posInicio    = d.origen.y-d.origen.altura/2-MARGEN_TEXTO/2;

                        var nro_puerto = 0;
                        for (var k = 0; k < acciones.length; k++) {
                            if (acciones[k].id == d.destino.id) {
                                nro_puerto = acciones[k].puerto;
                            }
                        }   

                        //  Posicion de salida en y desde a accion.
                        yOrig = posInicio+nro_puerto*espaciado_accion;
                        xOrig = d.origen.x;

                        if (cant_enlaces == 1) {
                            yOrig = d.origen.y
                        } 

                        var tamLineaHoriz;

                        if (d.origen.x <= d.destino.x) {
                            tamLineaHoriz = 50*(acciones.length-i);
                        } else {
                            tamLineaHoriz = -50*(acciones.length-i);
                        }
                    
                        // Buscamos el puerto asignado en la vista.
                        vistas = [];
                        if (d.origen.y <= d.destino.y) {
                            vistas = info_vistas[d.destino.id].rela_abajo;
                        } else {
                            vistas = info_vistas[d.destino.id].rela_arriba;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < vistas.length; k++) {
                            if (vistas[k].id == d.origen.id) {
                                nro_puerto = vistas[k].puerto;
                            }
                        }   

                        var cant_enlaces    = vistas.length;
                        var espaciado_vista = (d.destino.ancho-2*MARGEN_TEXTO)/cant_enlaces;
                        var posInicio       = d.destino.x - d.destino.ancho/2 - MARGEN_TEXTO;


                        if (d.origen.y >= d.destino.y - d.destino.altura &&  d.origen.y <= d.destino.y) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else if (d.origen.y <= d.destino.y + d.destino.altura && d.origen.y > d.destino.y) {
                            yDest = d.destino.y + d.destino.altura/2;
                        } else if (d.origen.y < d.destino.y - d.destino.altura) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else {
                            yDest = d.destino.y + d.destino.altura/2;
                        }

                        xDest = posInicio+nro_puerto*espaciado_vista;

                        if (cant_enlaces == 1) { 
                            xDest = d.destino.x; 
                        }

                        // console.log("nombre",d.origen.nombre,"salida",id_salida,"puerto",nro_puerto, "altura", d.destino.altura, nro_puerto*espaciado);
                        //Guardamos la posicion donde parte el enlace.
                        d["x1"]=xOrig;
                        d["y1"]=yOrig;
                        
                        xDest = d.destino.x;

                        linea = "M"+xOrig+","+yOrig+
                                " L"+xDest+","+yOrig+
                                " L"+xDest+","+yDest;

                        //Guardamos la posicion donde llega el enlace.
                        d["x2"]=xDest;
                        d["y2"]=yDest;

                        return linea;
        });

        flechaV1.attr("points", function(d) {
                        var yDest, xDest;

                        // Buscamos el puerto asignado en la vista.
                        vistas = [];
                        if (d.origen.y <= d.destino.y) {
                            vistas = info_vistas[d.destino.id].rela_abajo;
                        } else {
                            vistas = info_vistas[d.destino.id].rela_arriba;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < vistas.length; k++) {
                            if (vistas[k].id == d.origen.id) {
                                nro_puerto = vistas[k].puerto;
                            }
                        }   

                        var cant_enlaces    = vistas.length;
                        var espaciado_vista = (d.destino.ancho-2*MARGEN_TEXTO)/cant_enlaces;
                        var posInicio       = d.destino.x - d.destino.ancho/2 - MARGEN_TEXTO;

                        if (d.origen.y >= d.destino.y - d.destino.altura &&  d.origen.y <= d.destino.y) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else if (d.origen.y <= d.destino.y + d.destino.altura && d.origen.y > d.destino.y) {
                            yDest = d.destino.y + d.destino.altura/2;
                        } else if (d.origen.y < d.destino.y - d.destino.altura) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else {
                            yDest = d.destino.y + d.destino.altura/2;
                        }

                        xDest = posInicio+nro_puerto*espaciado_vista;

                        if (cant_enlaces == 1) { 
                            xDest = d.destino.x; 
                        }
                        
                        if (d.origen.y <= d.destino.y) {
                            puntos = xDest+","+yDest+" "+(xDest-ALTURA_FLECHA/3)+","+(yDest-ALTURA_FLECHA)+" "+(xDest+ALTURA_FLECHA/3)+","+(yDest-ALTURA_FLECHA);                       
                        } else {
                            puntos = xDest+","+yDest+" "+(xDest-ALTURA_FLECHA/3)+","+(yDest+ALTURA_FLECHA)+" "+(xDest+ALTURA_FLECHA/3)+","+(yDest+ALTURA_FLECHA);
                        }
                        return puntos;
                    });

        enlaceAE.filter(function(d) {return d.origen.selected;})
            .attr("x1", function(d) {return d.origen.x;})
            .attr("y1", function(d) {return d.origen.y;});

        enlaceAE.filter(function(d) {return d.destino.selected;})
            .attr("x2", function(d) {return d.destino.x;})
            .attr("y2", function(d) {return d.destino.y;});


        enlaceEV.filter(function(d) {return d.origen.selected;})
                .attr("d", function(d, i) { 
                        var externos = [];
                        
                        // Buscamos el puerto asignado en el externo.
                        if (d.destino.x <= d.origen.x) {
                            externos = info_externos[d.origen.id].rela_izq;
                        } else {
                            externos = info_externos[d.origen.id].rela_der;
                        }

                        cant_enlaces = externos.length;
                        espaciado_externo = (d.origen.radio-MARGEN_TEXTO)/cant_enlaces;
                        posInicio    = d.origen.y-d.origen.radio+MARGEN_TEXTO/2;

                        var nro_puerto = 0;
                        for (var k = 0; k < externos.length; k++) {
                            if (externos[k].id == d.destino.id) {
                                nro_puerto = externos[k].puerto;
                            }
                        }   

                        //  Posicion de salida en y desde a accion.
                        yOrig = posInicio+nro_puerto*espaciado_externo;
                        xOrig = d.origen.x;

                        if (cant_enlaces == 1) {
                            yOrig = d.origen.y
                        } 

                        var tamLineaHoriz;

                        if (d.origen.x <= d.destino.x) {
                            tamLineaHoriz = 50*(externos.length-i);
                        } else {
                            tamLineaHoriz = -50*(externos.length-i);
                        }
                    
                        // Buscamos el puerto asignado en la vista.
                        vistas = [];
                        if (d.origen.y <= d.destino.y) {
                            vistas = info_vistas[d.destino.id].rela_abajo;
                        } else {
                            vistas = info_vistas[d.destino.id].rela_arriba;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < vistas.length; k++) {
                            if (vistas[k].id == d.origen.id) {
                                nro_puerto = vistas[k].puerto;
                            }
                        }   

                        var cant_enlaces    = vistas.length;
                        var espaciado_vista = (d.destino.ancho-2*MARGEN_TEXTO)/cant_enlaces;
                        var posInicio       = d.destino.x - d.destino.ancho/2 + MARGEN_TEXTO;

                        if (d.origen.y >= d.destino.y - d.destino.altura &&  d.origen.y <= d.destino.y) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else if (d.origen.y <= d.destino.y + d.destino.altura && d.origen.y > d.destino.y) {
                            yDest = d.destino.y + d.destino.altura/2;
                        } else if (d.origen.y < d.destino.y - d.destino.altura) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else {
                            yDest = d.destino.y + d.destino.altura/2;
                        }

                        xDest = posInicio+nro_puerto*espaciado_vista;

                        if (cant_enlaces == 1) { 
                            xDest = d.destino.x; 
                        }

                        //Guardamos la posicion donde parte el enlace.
                        d["x1"]=xOrig;
                        d["y1"]=yOrig;
                        
                        xDest = d.destino.x;

                        linea = "M"+xOrig+","+yOrig+
                                " L"+xDest+","+yOrig+
                                " L"+xDest+","+yDest;

                        //Guardamos la posicion donde llega el enlace.
                        d["x2"]=xDest;
                        d["y2"]=yDest;

                        return linea;
                    });

        enlaceEV.filter(function(d) {return d.destino.selected;})
                    .attr("d", function(d, i) { 
                        var externos = [];
                        
                        // Buscamos el puerto asignado en el externo.
                        if (d.destino.x <= d.origen.x) {
                            externos = info_externos[d.origen.id].rela_izq;
                        } else {
                            externos = info_externos[d.origen.id].rela_der;
                        }

                        cant_enlaces = externos.length;
                        espaciado_externo = (d.origen.radio-MARGEN_TEXTO)/cant_enlaces;
                        posInicio    = d.origen.y-d.origen.radio+MARGEN_TEXTO/2;

                        var nro_puerto = 0;
                        for (var k = 0; k < externos.length; k++) {
                            if (externos[k].id == d.destino.id) {
                                nro_puerto = externos[k].puerto;
                            }
                        }   

                        //  Posicion de salida en y desde a accion.
                        yOrig = posInicio+nro_puerto*espaciado_externo;
                        xOrig = d.origen.x;

                        if (cant_enlaces == 1) {
                            yOrig = d.origen.y
                        } 

                        var tamLineaHoriz;

                        if (d.origen.x <= d.destino.x) {
                            tamLineaHoriz = 50*(externos.length-i);
                        } else {
                            tamLineaHoriz = -50*(externos.length-i);
                        }
                    
                        // Buscamos el puerto asignado en la vista.
                        vistas = [];
                        if (d.origen.y <= d.destino.y) {
                            vistas = info_vistas[d.destino.id].rela_abajo;
                        } else {
                            vistas = info_vistas[d.destino.id].rela_arriba;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < vistas.length; k++) {
                            if (vistas[k].id == d.origen.id) {
                                nro_puerto = vistas[k].puerto;
                            }
                        }   

                        var cant_enlaces    = vistas.length;
                        var espaciado_vista = (d.destino.ancho-2*MARGEN_TEXTO)/cant_enlaces;
                        var posInicio       = d.destino.x - d.destino.ancho/2 + MARGEN_TEXTO;

                        if (d.origen.y >= d.destino.y - d.destino.altura &&  d.origen.y <= d.destino.y) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else if (d.origen.y <= d.destino.y + d.destino.altura && d.origen.y > d.destino.y) {
                            yDest = d.destino.y + d.destino.altura/2;
                        } else if (d.origen.y < d.destino.y - d.destino.altura) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else {
                            yDest = d.destino.y + d.destino.altura/2;
                        }

                        xDest = posInicio+nro_puerto*espaciado_vista;

                        if (cant_enlaces == 1) { 
                            xDest = d.destino.x; 
                        }

                        //Guardamos la posicion donde parte el enlace.
                        d["x1"]=xOrig;
                        d["y1"]=yOrig;
                        
                        xDest = d.destino.x;

                        console.log("Aquiiiiii222", d);

                        linea = "M"+xOrig+","+yOrig+
                                " L"+xDest+","+yOrig+
                                " L"+xDest+","+yDest;

                        //Guardamos la posicion donde llega el enlace.
                        d["x2"]=xDest;
                        d["y2"]=yDest;

                        return linea;
                    });

        flechaV2.attr("points", function(d) {
                        var yDest, xDest;

                        // Buscamos el puerto asignado en la vista.
                        vistas = [];
                        if (d.origen.y <= d.destino.y) {
                            vistas = info_vistas[d.destino.id].rela_abajo;
                        } else {
                            vistas = info_vistas[d.destino.id].rela_arriba;
                        }

                        var nro_puerto = 0;
                        for (var k = 0; k < vistas.length; k++) {
                            if (vistas[k].id == d.origen.id) {
                                nro_puerto = vistas[k].puerto;
                            }
                        }   

                        var cant_enlaces    = vistas.length;
                        var espaciado_vista = (d.destino.ancho-2*MARGEN_TEXTO)/cant_enlaces;
                        var posInicio       = d.destino.x - d.destino.ancho/2 - MARGEN_TEXTO;

                        if (d.origen.y >= d.destino.y - d.destino.altura &&  d.origen.y <= d.destino.y) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else if (d.origen.y <= d.destino.y + d.destino.altura && d.origen.y > d.destino.y) {
                            yDest = d.destino.y + d.destino.altura/2;
                        } else if (d.origen.y < d.destino.y - d.destino.altura) {
                            yDest = d.destino.y - d.destino.altura/2;
                        } else {
                            yDest = d.destino.y + d.destino.altura/2;
                        }

                        xDest = posInicio+nro_puerto*espaciado_vista;

                        if (cant_enlaces == 1) { 
                            xDest = d.destino.x; 
                        }
                        
                        if (d.origen.y <= d.destino.y) {
                            puntos = xDest+","+yDest+" "+(xDest-ALTURA_FLECHA/3)+","+(yDest-ALTURA_FLECHA)+" "+(xDest+ALTURA_FLECHA/3)+","+(yDest-ALTURA_FLECHA);                       
                        } else {
                            puntos = xDest+","+yDest+" "+(xDest-ALTURA_FLECHA/3)+","+(yDest+ALTURA_FLECHA)+" "+(xDest+ALTURA_FLECHA/3)+","+(yDest+ALTURA_FLECHA);
                        }
                        return puntos;
                    });


            enlaceAO.filter(function(d) {return d.origen.selected;})
                .attr("x1", function(d) {return d.origen.x;})
                .attr("y1", function(d) {return d.origen.y;});

            enlaceAO.filter(function(d) {return d.destino.selected;})
                .attr("x2", function(d) {return d.destino.x;})
                .attr("y2", function(d) {return d.destino.y;});
        }


    //-----------------------------------------------------------------------------
    //                               FIN DIAGRAMA
    //-----------------------------------------------------------------------------

        });

        const TAMANO_MAX_ATRIBUTO = 28;

        $scope.setTab = function(newTab) {
            $scope.tab = newTab;
        };
        $scope.isSet = function(tabNum) {
            return $scope.tab === tabNum;
        };
        $scope.VDiseno3 = function(idDiseno) {
            $location.path('/VDiseno/'+idDiseno);
        };
        $scope.VLogin3 = function() {
            $location.path('/VLogin');
        };
        $scope.ACambiarDiagrama1 = function(idDiagrama) {
            $location.path('/VDiagrama/'+idDiagrama)
        };
        $scope.fDiagramaSubmitted = false;
        $scope.AModificarDiagrama1 = function(isValid) {
            $scope.fDiagramaSubmitted = true;
            if (isValid) {

                diagramaService.AModificarDiagrama($scope.fDiagrama).then(function (object) {
                    var msg = object.data["msg"];
                    if (msg) flash(msg);
                    var label = object.data["label"];
                    $location.path(label);
                    $route.reload();
                });
            }
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
        $scope.AEliminarElemento1 = function(idNodo) {
            $('#modal-eliminar').modal('hide');
            
            elementoService.AEliminarElemento({"idNodo":((typeof idNodo === 'object')?JSON.stringify(idNodo):idNodo)}).then(function (object) {
                var msg = object.data["msg"];
                if (msg) flash(msg);
                var label = object.data["label"];
                $location.path(label);
                $route.reload();            
            });
        };
        $scope.agregar1 = function() {
            var id     = $scope.fElemento.atributos.length + 1;
            var nombre = $scope.fElemento.nombre_atributo;

            if (nombre.length > TAMANO_MAX_ATRIBUTO) {
                nombre = nombre.substr(0,TAMANO_MAX_ATRIBUTO);
            }

            var i   = 0;
            while (i < $scope.fElemento.atributos.length) {
                if ($scope.fElemento.atributos[i].id == id) {
                    id += 1;
                    i = $scope.fElemento.atributos.length;
                }
                i++;
            }
            if (nombre.length > 0) {
                $scope.fElemento.atributos.push({"id":id, "nombre": nombre, "accion_interna": 0, "accion_externa":0, "accion_anterior": 0, "atributos_eliminar": []});
            }
            $scope.fElemento.nombre_atributo = '';
        };
        $scope.eliminarAtributo1 = function(id) {
            var atributos = $scope.fElemento.atributos;

            var i = 0;
            var encontrado = false;
            while (i < atributos.length && !encontrado) {
                encontrado = atributos[i].id == id;
                i++;
            }

            if (encontrado) {
                atributos.splice(i-1,1);
            }
        }
        $scope.agregar2 = function() {
            var id     = $scope.fVista.atributos.length + 1;
            var nombre = $scope.fVista.nombre_atributo;

            if (nombre.length > TAMANO_MAX_ATRIBUTO) {
                nombre = nombre.substr(0,TAMANO_MAX_ATRIBUTO);
            }

            var i   = 0;
            while (i < $scope.fVista.atributos.length) {
                if ($scope.fVista.atributos[i].id == id) {
                    id += 1;
                    i = $scope.fVista.atributos.length;
                }
                i++;
            }

            if (nombre.length > 0) {
                $scope.fVista.atributos.push({"id":id, "nombre": nombre, "accion_interna": 0, "accion_externa":0, "accion_anterior": 0, "atributos_eliminar": []});
            }
            $scope.fVista.nombre_atributo = '';
        };

        $scope.atributo_selecionado_id = 0;
        $scope.setAtributo = function(id, i) {
            var atributos = $scope.fVista.atributos;
            $scope.atributo_selecionado_id = id;
            $scope.fVista.accion_interna = atributos[i].accion_interna;
            $scope.fVista.accion_externa = atributos[i].accion_externa;
            $scope.fVista.nombre_atr = atributos[i].nombre;
        };
        $scope.asociar1 = function() {
            var atributos = $scope.fVista.atributos;

            for (var i = 0; i < atributos.length; i++) {
                var anterior  = atributos[i].accion_externa;

                if(atributos[i].id ==  $scope.atributo_selecionado_id) {
                    atributos[i].nombre = $scope.fVista.nombre_atr;
                    atributos[i].accion_interna = $scope.fVista.accion_interna;
                    atributos[i].accion_externa = $scope.fVista.accion_externa;

                    if ($scope.fVista.accion_externa == 0) {
                        atributos[i].accion_anterior = anterior;
                    }
                }
            }
        };
        $scope.eliminarAtributo2 = function(id) {
            var atributos = $scope.fVista.atributos;

            var i = 0;
            var encontrado = false;
            while (i < atributos.length && !encontrado) {
                encontrado = atributos[i].id == id;
                i++;
            }

            if (encontrado) {
                $scope.fVista.atributos_eliminar.push(atributos[i-1]);
                atributos.splice(i-1,1);
            }
        }
        $scope.agregar3 = function() {
            if ($scope.fAccion.vista_interna != 0) {
                
                // Buscamos si ya la vista fue agregada.
                var i = 0;
                var tam_relaciones_internas = $scope.fAccion.relaciones_internas.length;
                var existe = false;
                while (i < tam_relaciones_internas && !existe) {
                    if ($scope.fAccion.relaciones_internas[i].idVista == $scope.fAccion.vista_interna) {
                        existe = true;
                    }
                    i++;
                }

                if (!existe) {
                    // Buscamos el nombre de la vista.
                    var j = 0;
                    var nombre = '';
                    while (j < $scope.res.fAccion_opcionesVistaInterna.length) {

                        if ($scope.res.fAccion_opcionesVistaInterna[j].key == $scope.fAccion.vista_interna) {
                            nombre = $scope.res.fAccion_opcionesVistaInterna[j].value;
                            j = $scope.res.fAccion_opcionesVistaInterna.length;
                        }
                        j++;
                    }
                    $scope.fAccion.relaciones_internas.push({"idVista": $scope.fAccion.vista_interna,  "nombre": nombre});
                }
            }
            $scope.fAccion.vista_interna = 0;
        };
        $scope.eliminarVistaInterna1 = function(id) {
            var relaciones = $scope.fAccion.relaciones_internas;
            
            var i = 0;
            var encontrado = false;
            while (i < relaciones.length && !encontrado) {
                encontrado = relaciones[i].idVista == id;
                i++;
            }

            if (encontrado) {
                $scope.fAccion.rela_internas_eliminar.push(id);
                relaciones.splice(i-1,1);
            }
        };
        $scope.agregar4 = function() {
            if ($scope.fAccion.vista_externa != 0) {
                // Buscamos si ya la vista fue agregada.
                var i = 0;
                var tam_relaciones_externas = $scope.fAccion.relaciones_externas.length;
                var existe = false;
                while (i < tam_relaciones_externas && !existe) {
                    if ($scope.fAccion.relaciones_externas[i].nodo_real == $scope.fAccion.vista_externa) {
                        existe = true;
                    }
                    i++;
                }

                if (!existe) {
                    // Buscamos el nombre de la vista.
                    var j = 0;
                    var nombre = '';
                    while (j < $scope.res.fAccion_opcionesVistaExterna.length) {

                        if ($scope.res.fAccion_opcionesVistaExterna[j].key == $scope.fAccion.vista_externa) {
                            nombre = $scope.res.fAccion_opcionesVistaExterna[j].value;
                            j = $scope.res.fAccion_opcionesVistaExterna.length;
                        }
                        j++;
                    }
                    $scope.fAccion.relaciones_externas.push({"idVista": $scope.fAccion.vista_externa,  "nombre": nombre, "nodo_real": $scope.fAccion.vista_externa});
                }
            }
            $scope.fAccion.vista_externa = 0;
        };
        $scope.eliminarVistaExterna1 = function(id) {
            var relaciones = $scope.fAccion.relaciones_externas;
            
            var i = 0;
            var encontrado = false;
            while (i < relaciones.length && !encontrado) {
                encontrado = relaciones[i].nodo_real == id;
                i++;
            }

            if (encontrado) {
                $scope.fAccion.rela_externas_eliminar.push(id);
                relaciones.splice(i-1,1);
            }
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