# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from marker import Marker
from util import *
import pyowm
import foursquare


app = Flask(__name__)
#Open Weather Map API key
owm = pyowm.OWM('476b567996e1e53918e3a58f1b23f5ad')
#Foursquare API key
fq = foursquare.Foursquare(client_id='LDLO5MZD3ZDXOKKKPERTWS1SNVBJBAYZVZFYYDQFB052KB5S', client_secret='UZ4IWPRCI2HZKTENOCKV2MS1X3QMWDET0D3CFXVL52YWKRTC')

def mainStatus(status):
    if status == 'snow':
        return 'snowy'
    elif status == 'rain':
        return 'rainy'
    elif status == 'clear':
        return 'sunny'
    elif status == 'clouds':
        return 'cloudy'

#use index.html for application
@app.route('/')
def index():
	return render_template('index.html')


@app.route('/search/<name>')
def search(name):
	observation = owm.weather_at_place(name)
	weather = observation.get_weather()
	location = observation.get_location()
	#set weather status to obtain search keyword for foursquare
	status = mainStatus(str(weather.get_status()))
	#search in the tips according to status keyword and coordinates
	places = fq.tips.search(params={'query': status, 'll': str(location.get_lat()) + ',' + str(location.get_lon())})
	tips = places['tips']
	temp = temp = weather.get_temperature(unit='celsius')
	w = 'Temperature(celsius): '+ str(temp['temp']) + ' Humidity(%): ' + str(weather.get_humidity())
	markers = []
	#for every venue create a marker object
	for tip in tips:
		markers.append(Marker(tip['venue']['name'], tip['venue']['location'], tip['text']))
	#get searched city's longitude and latitude information
	center = {'lat' : location.get_lat(), 'lng' : location.get_lon()}
	result = {'weather' : w, 'stats' : status, 'center' : center, 'markers' : markers}
	#This function will produce JSON-formatted string for a dictionary that have instances of custom classes as leaves
	return json_repr(result)

if __name__ == "__main__":
	app.debug = True
	app.run()
