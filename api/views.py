import json
from django.shortcuts import render
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis import geos
from django.contrib.gis import measure
from geopy.distance import distance as geopy_distance
from django.contrib.auth.decorators import login_required
from api import models

# from django.contrib.auth import logout


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
        d = geopy_distance(currentPoint, restaurant['fields']['location']).kilometers
        d = round(d, 2)
        restaurant['fields']['distance'] = d

        # Fancy splitting on POINT(lon, lat)
        lng = restaurant['fields']['location'].split()[1][1:]
        lat = restaurant['fields']['location'].split()[2][:-1]

        del restaurant['fields']['location']
        restaurant['fields']['lng'] = lng
        restaurant['fields']['lat'] = lat

    return HttpResponse(json.dumps({"response":{"total": len(data),"venues": data}}),  mimetype='application/json')

def closest(request):
    restaurants = []
    if request.method == 'GET' and 'lat' in request.GET and 'lon' in request.GET:
        
        lat = float(request.GET['lat'])
        lon = float(request.GET['lon'])
        return getRestaurants(lon, lat)
    else:
        return HttpResponse('Request method not correct')

@login_required
def comment(request, rest_pk):
    '''
    rest_pk must be valid one for existing restaurant or 
    ValueError will be raised on save() attempt in POST part. 
    '''
    context = {}
    try:
        rest = models.Restaurant.objects.get(id=rest_pk)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == u'GET':
        try:
            filterargs = { 'restaurant': rest, 'user': request.user }
            comment = models.Comment.objects.get(**filterargs)
            context['comment_text'] = comment.text
        except ObjectDoesNotExist:
            pass


    if request.method == u'POST':
        filterargs = { 'restaurant': rest, 'user': request.user }
        comment, is_created = models.Comment.objects.get_or_create(**filterargs)
        comment.text = request.POST[u'comment']
        if is_created:
            comment.user = request.user
            comment.restaurant = rest
        comment.save()
        context['comment_text'] = comment.text

    context.update(csrf(request))
    return render_to_response('comment.html', context)

def show_all_comments(request, rest_pk):
    try:
        rest = models.Restaurant.objects.get(id=rest_pk)
    except ObjectDoesNotExist:
        raise Http404

    comments = models.Comment.objects.filter(restaurant=rest)
    data = serializers.serialize('json', comments)
    data = json.loads(data)
    return HttpResponse(json.dumps({"response":{"total": len(data), "comments": data}}),  mimetype='application/json')

@login_required
def tip(request, rest_pk):
    '''
    rest_pk must be valid one for existing restaurant or 
    ValueError will be raised on save() attempt in POST part. 
    '''
    context = {}
    try:
        rest = models.Restaurant.objects.get(id=rest_pk)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == u'GET':
        try:
            filterargs = { 'restaurant': rest, 'user': request.user }
            tip = models.Tip.objects.get(**filterargs)
            context['tip_text'] = tip.text
        except ObjectDoesNotExist:
            pass


    if request.method == u'POST':
        filterargs = { 'restaurant': rest, 'user': request.user }
        tip, is_created = models.Tip.objects.get_or_create(**filterargs)
        tip.text = request.POST[u'tip']
        if is_created:
            tip.user = request.user
            tip.restaurant = rest
        tip.save()
        context['tip_text'] = tip.text

    context.update(csrf(request))
    return render_to_response('tip.html', context)

def show_all_tips(request, rest_pk):
    try:
        rest = models.Restaurant.objects.get(id=rest_pk)
    except ObjectDoesNotExist:
        raise Http404

    tips = models.Tip.objects.filter(restaurant=rest)
    data = serializers.serialize('json', tips)
    data = json.loads(data)
    return HttpResponse(json.dumps({"response":{"total": len(data), "tips": data}}),  mimetype='application/json')

# @login_required
# def log_out(request):
#     logout(request)
#     return render(request, "comment.html")
