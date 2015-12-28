// var wiki = 'https://en.wikipedia.org/w/api.php?action=opensearch&search=%content%&format=json&callback=wikiCallback';
var wiki = 'https://en.wikipedia.org/w/api.php?format=json&action=query&titles=%content%&prop=revisions&rvprop=content';
var objToday = new Date(),
            weekday = new Array('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
            dayOfWeek = weekday[objToday.getDay()],
            domEnder = new Array( 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th' ),
            // domEnder = new Array( 'th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th' ),
            dayOfMonth = today + (objToday.getDate() < 10) ? '0' + objToday.getDate() + domEnder[objToday.getDate()] : objToday.getDate() + domEnder[parseFloat(("" + objToday.getDate()).substr(("" + objToday.getDate()).length - 1))],
            months = new Array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'),
            curMonth = months[objToday.getMonth()],
            curYear = objToday.getFullYear(),
            curHour = objToday.getHours() > 12 ? objToday.getHours() - 12 : (objToday.getHours() < 10 ? "0" + objToday.getHours() : objToday.getHours()),
            curMinute = objToday.getMinutes() < 10 ? "0" + objToday.getMinutes() : objToday.getMinutes(),
            curSeconds = objToday.getSeconds() < 10 ? "0" + objToday.getSeconds() : objToday.getSeconds(),
            curMeridiem = objToday.getHours() > 12 ? "PM" : "AM";
var today = dayOfWeek + " " + dayOfMonth + " of " + curMonth + ", " + curYear;

function loadData(){
	// alert("I am an alert box!");
	var $weather = $('#weather');

	ipapi_url = "http://ip-api.com/json";
	$.getJSON(ipapi_url, function(data){
		var lat = data.lat;
		var lon = data.lon;
		$weather.append('<div>' + data.isp + ', ' + data.city + ', ' + data.regionName + ', ' + data.country + '</div>');
		$('#province').val(data.regionName);
		$('#city').val(data.city);
		getWeather(lat, lon);
		getMap(data.isp, data.city);
		
	}).error(function(e){
		alert("Error!");
	});
}

function getWeather(lat, lon){
	var $weather = $('#weather');
	open_weather_map = "http://api.openweathermap.org/data/2.5/weather?lat=%LAT%&lon=%LON%&appid=a8f34ed851c81648ff3d2c426b41a376".replace("%LAT%",lat).replace("%LON%",lon);
	$.getJSON(open_weather_map, function(data){
		var minTem = "Minimum temperature: " + (data.main.temp_min - 273).toFixed(2) + " Celsius";
		var maxTem = "Maximum temperature: " + (data.main.temp_max - 273).toFixed(2) + " Celsius";
		var description = "Weather condition: " + data.weather[0].description;
		var wind = "Wind Speed: " + data.wind.speed + " Meter/Sec";
		$weather.append('<div>' + minTem +'</div>');
		$weather.append('<div>' + maxTem +'</div>');
		$weather.append('<div>' + description +'</div>');
		$weather.append('<div>' + wind +'</div>');
	}).error(function(e){
	});
}

function getMap(isp, city){
	var $weather = $('#weather');
	var $map = $('#map');
	isp = isp.replace(/ /g, "+");
	city = city.replace(/ /g, "+"); 
	GMAPS_URL = "http://maps.google.com/maps/api/staticmap?size=380x380&center=%isp%,%city%&zoom=15&sensor=false".replace("%isp%", isp).replace("%city%", city);
	$map.append('<img id = "map" src = %url%>'.replace("%url%", GMAPS_URL));

}

function loadWikiEvents(){
	var $events = $('#events');
	var $births = $('#births');
	var $holidays = $('#holidays');

	currentDate_event = (curMonth + "_" + dayOfMonth).replace("th", "");
	wiki_events = wiki.replace("%content%", currentDate_event);

    var wikitimeout = setTimeout(function(){
    	$events.text("fail");
    },8000);

    $.ajax({

    	url:wiki_events,
    	dataType:"jsonp",
    	success: function(response){
    		var pages = response["query"]["pages"]
    		var keys = Object.keys(pages);
    		var content = String(pages[keys]["revisions"][0]["*"]);
    		var index_events = content.indexOf("==Events==");
    		var index_births = content.indexOf("==Births==");
    		var index_deaths = content.indexOf("==Deaths==");
    		var index_holidays = content.indexOf("==Holidays and observances==");
    		var index_references = content.indexOf("==References==");
    		var index_external = content.indexOf("==External links==");
    		
    		events = content.substring(index_events,index_births).replace(/\[/g,"").replace(/\]/g,"").split('\n');
    		births = content.substring(index_births,index_deaths).replace(/\[/g,"").replace(/\]/g,"").split('\n');
    		
    		if (index_references >0){
    			holidays = content.substring(index_holidays,index_references).replace(/\[/g,"").replace(/\]/g,"").split('\n');
    		} else{
    			holidays = content.substring(index_holidays,index_external).replace(/\[/g,"").replace(/\]/g,"").split('\n');
    		}

    		for (var i = 0; i < 10; i++){
    			$events.append(events[i] + "<br>");
    		}
    		$events.append("<div> <a class = 'more' href='https://en.wikipedia.org/wiki/%content%'> more </a> </div>".replace("%content%",currentDate_event+"#Events"));
    		$events.prepend("<div> Source: <a class = 'source' href = 'https://www.wikipedia.org/'>Wikipedia </a></div> <br>");

    		for (var i = 0; i < 10; i++){
    			$births.append(births[i] + "<br>");
    		}
    		$births.append("<div class = 'more'> <a href='https://en.wikipedia.org/wiki/%content%'> more </a> </div>".replace("%content%",currentDate_event+"#Births"));
    		$births.prepend("<br><br>")

    		for (var i = 0; i < holidays.length; i++){
    			$holidays.append(holidays[i] + "<br>");
    		}
    		$holidays.append("<div class = 'more'> <a href='https://en.wikipedia.org/wiki/%content%'> more </a> </div>".replace("%content%",currentDate_event+"#Holidays_and_observances"));
    		$holidays.prepend("<br><br>")
    		clearTimeout(wikitimeout);
    	}

    });
}


function loadNYT(){
	var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');

    var currentprovince = $('#province').val();
    var currentCity = $('#city').val();    
	NYTURL = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q='+currentCity +'+' + currentprovince +'&page=2&sort=oldest&api-key=dff1a8407c15258bfc80ef76a5936b3d:12:73559609'
    $.getJSON(NYTURL, function(data){
    	$nytHeaderElem.text(currentCity + " news in The New York Times");
    	articles = data.response.docs;
    	for (var i =0 ;i<articles.length;i++){
    		var article = articles[i];
    		$nytElem.append('<li class = "article">' + '<a href="' + article.web_url + '">' + article.headline.main+'</a>' + '<p>' + article.snippet + '</p>' + '</li>');
    	};
    }).error(function(e){
    	   $nytHeaderElem.text("What?!");
    });	
	return false;
};

function news(){
    $("#dialog").dialog();
}

// function getLocation(){
// 	ipapi_url = "http://ip-api.com/json";
// 	var city;
// 	var region;

// 	$.getJSON(ipapi_url, function(data){
// 			console.log(city);
// 		return data.city;
// 		region = data.regionName;
// 	}).error(function(e){
// 		alert("Error!");
// 	});
// 	return city;
// };

if (window.location.protocol != "http:")
    window.location.href = "http:" + window.location.href.substring(window.location.protocol.length)
loadData();
loadWikiEvents();
$('#form-container').submit(loadNYT);
$('#dialog').dialog();