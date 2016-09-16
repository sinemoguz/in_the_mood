# -*- coding: utf-8 -*-
import unicodedata

#This class is for Marker objects which will be pinned on Google Maps
class Marker:
	def __init__(self, title, location, tip):
		self.position = {'lat' : location['lat'], 'lng' : location['lng']}
		self.title =unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore')
		self.tip = unicodedata.normalize('NFKD', tip).encode('ASCII', 'ignore')
