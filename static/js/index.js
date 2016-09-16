var map;

function toggleBounce() {
  if (marker.getAnimation() !== null) {
    marker.setAnimation(null);
  } else {
    marker.setAnimation(google.maps.Animation.BOUNCE);
  }
}


function initMap(result) {
	var mapOptions = {
		zoom: 10,
		center: result.center
	}

	map = new google.maps.Map(document.getElementById("map"), mapOptions);

	result.markers.forEach(function(entry) {
		var marker = new google.maps.Marker({
			map: map,
			position: entry.position,
			title: entry.title.replace(/'/g, ""),
			animation: google.maps.Animation.DROP,
		});

		var contentString =  '<div id="content">'+
      						 '<font color="black">'+'<p><b>'+entry.title.replace(/'/g, "")+'</b>'+'</font>'+ 
      						 '</div>'+ 
      						 '<div id="bodyContent">'+
      						 '<font color="black">'+'<p><b>Tips:</b> '+entry.tip.replace(/'/g, "")+'</font>'+ 
      						 '</div>';


		var infowindow = new google.maps.InfoWindow({
    		content: contentString,
    		maxWidth: 200
  		});

  		marker.addListener('click', function() {
    		infowindow.open(map, marker);
  		},toggleBounce);
	});

	// Resize when page size changed
	google.maps.event.addDomListener(window, "resize", function() {
		length = $(".input-group").width();
		$("#map").height(length);
		$("#map").width(length)
	});

	// Get the search bar length and assign to map size
	length = $(".input-group").width();
	$("#map").height(length);
	$("#map").width(length);

	// Write weather status
	$("#weather-w").html("Weather is " + result.stats.replace(/'/g, ""));
	$("#stats-status").html(result.weather.replace(/'/g, ""));
}

function loadMap() {
	var name = $('#search-input').val();
	$.get("search/" + name, function(data){initMap(JSON.parse(data));});
}

$(document).on({
	ajaxStart: function(){$("body").addClass("loading");},
	ajaxStop: function(){$("body").removeClass("loading");}
});