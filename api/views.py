from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core import serializers
import json
from django.contrib.gis import geos
from django.contrib.gis import measure
from geopy.distance import distance as geopy_distance
from api import models


# Create your views here.
def getRestaurants(longitude, latitude):
	currentPoint = geos.GEOSGeometry('POINT(%s %s)' %(longitude, latitude))
	distance_m = 5000
	restaurants = models.Restaurant.gis.filter(location__distance_lte=(currentPoint, distance_m))
	restaurants = restaurants.distance(currentPoint).order_by('distance')

	# Removing your own self from the list.
	restaurants = restaurants[1:]

	# String based JSON
	data = serializers.serialize('json', restaurants)
	# Actual JSON object to be edited
	data = json.loads(data)

	for restaurant in data:
		restaurant['fields']['distance'] = geopy_distance(currentPoint, restaurant['fields']['location']).kilometers
		
		# Fancy splitting on POINT(lon, lat)
		lng = restaurant['fields']['location'].split()[1][1:]
		lat = restaurant['fields']['location'].split()[2][:-1]

		del restaurant['fields']['location']
		restaurant['fields']['lng'] = lng
		restaurant['fields']['lat'] = lat

	return HttpResponse(json.dumps(data))

def closest(request):
    restaurants = []
    if request.method == 'GET' and 'lat' in request.GET and 'lon' in request.GET:
    	
    	lat = float(request.GET['lat'])
    	lon = float(request.GET['lon'])
    	return getRestaurants(lon, lat)
    else:
    	return HttpResponse('Request method not correct')