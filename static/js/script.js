function loadData(){
	// alert("I am an alert box!");

	var $weather = $('#weather');

	ipapi_url = "http://ip-api.com/json";
	$.getJSON(ipapi_url, function(data){
		var lat = data.lat;
		var lon = data.lon;
		$weather.append('<div>' + data.isp + ', ' + data.city + ', ' + data.regionName + ', ' + data.country + '</div>');


	}).error(function(e){
		alert("Error!");
	});
}


loadData();