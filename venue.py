from flask import Flask
from flask import render_template
from marker import Marker
from util import *
import pyowm
import foursquare


app = Flask(__name__)
#Open Weather Map API key
owm = pyowm.OWM('476b567996e1e53918e3a58f1b23f5ad')
fq = foursquare.Foursquare(client_id='LDLO5MZD3ZDXOKKKPERTWS1SNVBJBAYZVZFYYDQFB052KB5S', client_secret='UZ4IWPRCI2HZKTENOCKV2MS1X3QMWDET0D3CFXVL52YWKRTC')

#use index.html for application
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search/<name>')
def search(name):
	observation = owm.weather_at_place(name)
	location = observation.get_location()
	#places = fq.venues.search(params={'ll': str(location.get_lat()) + ',' + str(location.get_lon())})
	tips = fq.tips.search(params={'ll': str(location.get_lat()) + ',' + str(location.get_lon())})
	#print places
	print tips


	return json_repr(tips)

if __name__ == "__main__":
	app.debug = True
	app.run()