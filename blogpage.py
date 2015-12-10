# -*- coding: utf-8 -*-
import os
import webapp2
import handler
import blogutils
import urllib
import json
from google.appengine.ext import db

def get_ipapi():
	ipapi_url = "http://ip-api.com/json" 
	try:
		content = urllib.urlopen(ipapi_url).read()
	except URLRrror:
		return
	return content	

def get_weather(lat, lon):
	open_weather_map = "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=a8f34ed851c81648ff3d2c426b41a376" % (lat,lon)
	try:
		content = urllib.urlopen(open_weather_map).read()
	except URLRrror:
		return
	return content

def gmaps_img(isp, city):
	isp = isp.replace(" ", "+")
	city = city.replace(" ", "+")
	GMAPS_URL = "http://maps.google.com/maps/api/staticmap?size=380x380&center=%s,%s&zoom=15&sensor=false" % (isp,city)
	print GMAPS_URL
	# print marker
	# print GMAPS_URL + marker
	return GMAPS_URL

class BlogPage(handler.Handler):
	"""the main page of travel-blog"""
	def render_blogpage(self, all_blogs = "", username = "", location_weather = "", img_url = ""):
		self.render("blogpage.html", username = username, all_blogs = all_blogs , location_weather = location_weather, img_url= img_url)

	def get(self):
		location_weather = []
		ip_content_json = get_ipapi()
		ip_content_dic = json.loads(ip_content_json)

		location = ip_content_dic["isp"] + ", " + ip_content_dic["city"] + ", " + ip_content_dic["regionName"] + ", " + ip_content_dic["country"]
		location_weather.append(location)

		open_weather_json = get_weather(ip_content_dic["lat"], ip_content_dic["lon"])
		weather_content_dic = json.loads(open_weather_json)

		img_url = gmaps_img(ip_content_dic["isp"], ip_content_dic["city"])


		location_weather.append("Minimum temperature: " + str(int(weather_content_dic["main"]["temp_min"]) - 273) + " Celsius")
		location_weather.append("Maximum temperature: " + str(int(weather_content_dic["main"]["temp_max"]) - 273) + " Celsius")
		location_weather.append("Weather condition: " + str(weather_content_dic["weather"][0]["description"]))
		location_weather.append("Wind Speed: "+ str(weather_content_dic["wind"]["speed"]) + " Meter/Sec")		

		all_blogs = blogutils.get_all_blogs()
		username = blogutils.checkcookie(self.request.cookies.get('username'))
		if username:
			self.render_blogpage(all_blogs,username, location_weather, img_url)
			return
		self.render_blogpage(all_blogs, "" ,location_weather, img_url)


'''
"as":"AS12093 University of Waterloo",
"city":"Waterloo",
"country":"Canada",
"countryCode":"CA",
"isp":"University Of Waterloo",
"lat":43.4715,
"lon":-80.5454,
"org":"University Of Waterloo",
"query":"129.97.124.187",
"region":"ON",
"regionName":"Ontario",
"status":"success",
"timezone":"America/Toronto",
"zip":"N2L"
'''

'''
"coord":{"lon":-80.52,
		 "lat":43.47},
"weather":[{"id":701,
		  "main":"Mist",
		  "description":
		  "mist",
		  "icon":"50d"}],
"base":"cmc stations",
"main":{"temp":279.3,
	    "pressure":1009,
	    "humidity":100,
	    "temp_min":278.15,
	    "temp_max":281.15},
"wind":{"speed":4.6,
		"deg":190},
"clouds":{"all":90},
"dt":1449766140,
"sys":{"type":1,
	   "id":3730,
	   "message":0.0032,
	   "country":"CA",
	   "sunrise":1449751464,
	   "sunset":1449783946},
"id":6176823,
"name":"Waterloo",
"cod":200}
'''