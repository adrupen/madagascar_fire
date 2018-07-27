/*

	JS file for the Madagascar Web Portal

 */

var params = {
	location: "",
	fire_magnitude: "",
	flora_damage: "",
	fauna_damage: ""
};

function sendToGEOSS(values){
	var http = new XMLHttpRequest();
	var url = "http://127.0.0.1:8089";
	var params = "";

	for (var param in values) {
		if (values.hasOwnProperty(param)) {
			params += "&" + param + "=" + values[param];
		}
	}

	http.open("POST", url, true);

	//Send the proper header information along with the request
	http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

	http.onreadystatechange = function() {//Call a function when the state changes.
		if(http.readyState == 4 && http.status == 200) {
			console.log(http.responseText);
		}
	};
	console.log("params sent: "+params);
	http.send(params);
}

function applyMargins() {
	var leftToggler = $(".mini-submenu-left");
	var rightToggler = $(".mini-submenu-right");

	if (leftToggler.is(":visible")) {
		$("#map .ol-zoom")
			.css("margin-left", 0)
			.removeClass("zoom-top-opened-sidebar")
			.addClass("zoom-top-collapsed");
	} else {
		$("#map .ol-zoom")
			.css("margin-left", $(".sidebar-left").width())
			.removeClass("zoom-top-opened-sidebar")
			.removeClass("zoom-top-collapsed");
	}
	if (rightToggler.is(":visible")) {
		$("#map .ol-rotate")
			.css("margin-right", 0)
			.removeClass("zoom-top-opened-sidebar")
			.addClass("zoom-top-collapsed");
	} else {
		$("#map .ol-rotate")
			.css("margin-right", $(".sidebar-right").width())
			.removeClass("zoom-top-opened-sidebar")
			.removeClass("zoom-top-collapsed");
	}
}

function isConstrained() {
	return $("div.mid").width() == $(window).width();
}

function applyInitialUIState() {
	if (isConstrained()) {
		$(".sidebar-left .sidebar-body").fadeOut('slide');
		$(".sidebar-right .sidebar-body").fadeOut('slide');
		$('.mini-submenu-left').fadeIn();
		$('.mini-submenu-right').fadeIn();
	}
}

$(document).ready(function() {

	$('.sidebar-left .slide-submenu').on('click',function() {
		var thisEl = $(this);
		thisEl.closest('.sidebar-body').fadeOut('slide',function(){
			$('.mini-submenu-left').fadeIn();
			applyMargins();
		});
	});

	$('.mini-submenu-left').on('click',function() {
		var thisEl = $(this);
		$('.sidebar-left .sidebar-body').toggle('slide');
		thisEl.hide();
		applyMargins();
	});

	$('.sidebar-right .slide-submenu').on('click',function() {
		var thisEl = $(this);
		thisEl.closest('.sidebar-body').fadeOut('slide',function(){
			$('.mini-submenu-right').fadeIn();
			applyMargins();
		});
	});

	$('.mini-submenu-right').on('click',function() {
		var thisEl = $(this);
		$('.sidebar-right .sidebar-body').toggle('slide');
		thisEl.hide();
		applyMargins();
	});

    $(window).on("resize", applyMargins);

	var map = L.map('map', {
		maxZoom: 17,
		zoomControl: false,
		attributionControl: false
	}).setView([-19.295335049096263,46.57384179999997], 6);

	var mapgrey = L.tileLayer('http://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
		attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy;<a href="https://carto.com/attribution">CARTO</a>'
	});

	var mapsat = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		id: 'christianlanger.lin45e75',
		accessToken: 'pk.eyJ1IjoiY2hyaXN0aWFubGFuZ2VyIiwiYSI6InJOMFAxS00ifQ.tt_H4EfT3ccRSPrkD0KKRQ'
	}).addTo(map);

	var baseLayers = {
		"Grayscale": mapgrey,
		"Satellite": mapsat
	};

	var layerSwitcher = L.control.layers(baseLayers, null, {
		collapsed: false,
		position: 'bottomright'
	}).addTo(map);

	applyInitialUIState();
	applyMargins();

	// Create group for your layers and add it to the map
	var layerGroup = L.layerGroup().addTo(map);

	// MODIS active fires last 24 hrs
	var modisfire24 = L.tileLayer.wms('https://firms.modaps.eosdis.nasa.gov/wms/?', {
		layers: 'fires_viirs_24',
		zIndex: 1020,
		format: 'png'
	});

	$("#modisfire24").click(function() {
		if(document.getElementById('modisfire24').checked){
			layerGroup.addLayer(modisfire24);
		} else{
			layerGroup.removeLayer(modisfire24);
		}
	}); 

	//MODIS active fires last 48 hrs
	var modisfire48 = L.tileLayer.wms('https://firms.modaps.eosdis.nasa.gov/wms/?', {
		layers: 'fires_viirs_48',
		zIndex: 1020,
		format: 'png'
	});

 // CAMS JADE
 // var modisfire48 = L.tileLayer.wms('http://geoserver.webservice-energy.org/geoserver/cams_jade/wms?', {
 //    layers: 'CAMS_JADE_monthly_GHI_2005_01',
 //    zIndex: 1020,
 //    format: 'png'
 //    });

	$("#modisfire48").click(function() {
		if(document.getElementById('modisfire48').checked){
			layerGroup.addLayer(modisfire48);
		} else{
			layerGroup.removeLayer(modisfire48);
		}
	});

	// MODIS active fires last 72 hrs
	var modisfire72 = L.tileLayer.wms('https://firms.modaps.eosdis.nasa.gov/wms/?', {
		layers: 'fires_viirs_72',
		zIndex: 1020,
		format: 'png'
	});

	$("#modisfire72").click(function() {
		if(document.getElementById('modisfire72').checked){
			layerGroup.addLayer(modisfire72);
		} else{
			layerGroup.removeLayer(modisfire72);
		}
	});

	var flameIcon = L.icon({
		iconUrl: 'img/flame.png',

		iconSize:     [38, 38], // size of the icon
		shadowSize:   [50, 64], // size of the shadow
		iconAnchor:   [22, 34], // point of the icon which will correspond to marker's location
		shadowAnchor: [4, 62],  // the same for the shadow
		popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
	});


	// Initialise the FeatureGroup to store editable layers
	var editableLayers = new L.FeatureGroup();
	map.addLayer(editableLayers);

	// Initialise the draw control and pass it the FeatureGroup of editable layers
	var options = {
		position: 'bottomright',
		draw: {
			polyline: false,
			polygon: false,
			circle: false,
			rectangle: false,
			marker: {
				icon: flameIcon
				}
		},
		edit: {
			featureGroup: editableLayers 
		}
	};

	var drawControl = new L.Control.Draw(options);

	map.addControl(drawControl);
  
	map.on('draw:created', function (e) {
		var type = e.layerType,
		layer = e.layer;

		editableLayers.addLayer(layer);

		if (type === 'marker') {
			var curPos = layer.getLatLng(); 
			document.querySelector('#latlon').value = "(" + curPos.lat + "," + curPos.lng + ")";
		}
	});

    var dab = GIAPI.DAB('https://api.geodab.eu/dab');
    var paginator;
    var overlays = {};

    var beforeSearch = function(msg) {

		layerGroup.clearLayers();

		$('#report-title-select').empty();
		$('#report-title-ul').empty();
		//$('#add-layer-button').attr('disabled', 'disabled');
		$('#search-button').attr('disabled', 'disabled');
		$('#prev-button').attr('disabled', 'disabled');
		$('#next-button').attr('disabled', 'disabled');

		$('#info-label').html(msg);
    };


    var afterSearch = function(resultSet, paginator) {
		var info = '<p><br><b>' + resultSet.size + '</b> datasets found</p>';

		$('#search-button').removeAttr('disabled');

		if (resultSet.size) {

			info += '<p>Showing results ' + resultSet.start + ' to ' + (resultSet.start + resultSet.pageSize - 1) + '</p>';

			//$('.add-layer-button').removeAttr('disabled');

			if (paginator.prev()) {
				$('#prev-button').removeAttr('disabled');
			}

			if (paginator.next()) {
				$('#next-button').removeAttr('disabled');
			}
		}

		$('#info-label').html(info);
    };


    // Search GEO DAB
    // by click search default button

    $('#search-button').click(function() {

        beforeSearch('Fetching datasets ...');

        var searchTerm = $('#search-term-input').val();
        var constraints = {};

        if (searchTerm) {
            constraints.what = searchTerm;
        }

        var options = {
            "pageSize": 10
        };

        dab.discover(onResponse, constraints, options);
    });

    // by click loupe button
    $('#headerSearch').click(function() {

        beforeSearch('Searching GEOSS ...');
        var searchTerm = $('#search-term-input').val();

        // discover constraints
        var constraints = {};

        if (searchTerm) {
            constraints.what = searchTerm;
        }
        // set page size
        var options = {
            "pageSize": 10
        };

        // start discover
        dab.discover(onResponse, constraints, options);

    });

	$('#prev-button').click(function() {

		beforeSearch('Getting previous results ...');
		paginator.prev(onResponse, true);
	});


	$('#next-button').click(function() {

		beforeSearch('Getting next results ...');
		paginator.next(onResponse, true);
	});



	for ( var i = 0; i < overlays.length; i++) {

		$("#geoss-" + i).click(function() {
			if(document.getElementById("geoss-" + i).checked){
				layerGroup.addLayer(overlays[i]);
			} else{
				layerGroup.removeLayer(overlays[i]);
			}
	  	});
	}
    
    // defines discover response callback function
    var onResponse = function(response) {

        // retrieves the result set
        // only one result set is expected (discover not expanded) 
        var resultSet = response[0];

        if (resultSet.error) {
            console.log("Error occurred: " + resultSet.error);
            return;
        }

        // retrieves the paginator  
        paginator = resultSet.paginator;

        afterSearch(resultSet, paginator);

        // document.writeln(paginator);

        // prints the result set
        // document.writeln("<h3>- Result set -</h3>");
        // document.writeln("start:"+resultSet.start+"<br>"); 
        // document.writeln("size:"+resultSet.size+"<br>"); 
        // document.writeln("pageCount:"+resultSet.pageCount+"<br>"); 
        // document.writeln("pageIndex:"+resultSet.pageIndex+"<br>"); 
        // document.writeln("pageSize:"+resultSet.pageSize+"<br>"); 

        // the current paginator page (the first of the result set)
        var page = paginator.page();

        // printing page nodes
        // document.writeln("<h3>- Nodes of first result set page-</h3>"); 
        // document.writeln("<pre>"); 

        overlays = [];

        while (page.hasNext()) {

            // retrieving the next page node
            var node = page.next();

            // retrieving the node report
            var report = node.report();

            //document.writeln(JSON.stringify(report,null,4));

            //$('#report-title-select').append('<option value="' + overlays.length + '">' + report.title + '</option>');

            $('#report-title-ul').append('<li style="display:block" value="geoss-' + overlays.length + '"><div><div class="card">' + '<img class="card-img-top" src="'+ report.overview + '" alt="image thumbnail not found"' + '"><div class="card-block"><h4 class="card-title">'+ report.title +'</h4><div class="card-text">'+ report.description +'</div></div><div class="card-footer"><span><div class="checkbox" style="padding:0;margin-bottom:10px"><label class="switch"><input id="geoss-' + overlays.length + '" type="checkbox"><span class="slider round"></span></label></div></span></div></div></div></li><div>&nbsp;</div>');

            var url = report.online[0].url;
            var name = report.online[0].name;

            var geosslayer = L.tileLayer.wms(url, {
                format: 'image/png',
                transparent: true,
                layers: name,
                zIndex: 1020,
                title: name
            });

            overlays.push(geosslayer);

        }
    };

   	$("#yearSlider").slider({step: 20000, min: 0, max: 200000, value:0});
	$("#yearSlider .slider-handle").text($("input#yearSlider").val());

	$("#yearSlider").on("slide", function(slideEvt) {
  		$("#yearSlider .slider-handle").text(slideEvt.value);
	});

	$("#sendBtn").on("click", function(){
		params.location = $("#latlon").val();
		params.fire_magnitude = $("#yearSlider").val();
		params.flora_damage = $("#floraSlider").val();
		params.fauna_damage = $("#faunaSlider").val();
		sendToGEOSS(params);
	}); 
}); 
 