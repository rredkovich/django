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
from django.contrib.auth import login
from social.apps.django_app.utils import psa
from api import models, forms
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from geopy.geocoders import Nominatim
from urllib2 import URLError

# from django.contrib.auth import logout
def restaurants_lists(request):
    form = forms.AddressForm()
    restaurants = []
    latitude=""
    longitude=""
    if request.POST:
        form = forms.AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            category = form.cleaned_data['category']

            list_of_cats = []
            if category:
                try:
                    list_of_cats.append(models.Category.objects.get(name__icontains=category))
                except (MultipleObjectsReturned):
                    length = models.Category.objects.filter(name__icontains=category).__len__()
                    for l in range(length):
                        list_of_cats.append(models.Category.objects.filter(name__icontains=category)[l])
                except (ObjectDoesNotExist):
                    pass
            if not address:
                if list_of_cats:
                    restaurants = models.Restaurant.objects.filter(categories__in=list_of_cats)
                else:
                    restaurants = models.Restaurant.objects.all
            else:
                geocoder = Nominatim()
                location = geocoder.geocode(address)
                if location:
                    latitude= location.latitude
                    longitude=location.longitude
                    currentPoint = geos.GEOSGeometry('POINT(%s %s)' %(longitude, latitude))
                    distance_m = {'km': 15}
                    if list_of_cats:
                        restaurants = models.Restaurant.gis.filter(
                            location__distance_lte=(currentPoint, measure.D(**distance_m)), 
                            categories__in=list_of_cats
                            ).distance(currentPoint)
                    else:
                        restaurants = models.Restaurant.gis.filter(location__distance_lte=(currentPoint, measure.D(**distance_m))).distance(currentPoint)
        context = {'all_restaurants': restaurants,'form': form,'longitude': longitude, 'latitude' : latitude}
        return render(request, 'restaurantlist.html', context)
    else:
        context = {'all_restaurants': restaurants,'form': form,'longitude': longitude, 'latitude' : latitude}
        return render(request, 'restaurants.html', context)


def get_category(request):
    if request.is_ajax():
        cat = request.GET['term']
        categories = models.Category.objects.filter(name__icontains = cat )[:20]
        results = []
        for category in categories:
            cat_json = {}
            cat_json['id'] = category.id
            cat_json['value'] = category.name
            results.append(cat_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
def get_restaurants(longitude, latitude, categories):
    '''
    Returns objects at given point that satisfy set of categories, 
    or all of them if categories is empty.
    input:
        str longitude
        str latitude
        list categories
    output:
        list of dicts
    '''
    currentPoint = geos.GEOSGeometry('POINT(%s %s)' %(longitude, latitude))
    distance_m = 15000
    list_of_cats = []
    for c in categories:
        list_of_cats.append(models.Category.objects.get(name=c))
    if list_of_cats:
        restaurants = models.Restaurant.gis.filter(
            location__distance_lte=(currentPoint, distance_m), 
            categories__in=list_of_cats
            )
    else:
        restaurants = models.Restaurant.gis.filter(location__distance_lte=(currentPoint, distance_m))
    
    # seems that this thing doesn't actually order objects by distance
    # btw at this step there is no distance property in objects or rows in table
    # restaurants = restaurants.distance(currentPoint).order_by('distance')

    # String based JSON
    data = serializers.serialize('json', restaurants)
    # Actual JSON object to be edited
    data = json.loads(data)

    # if venue has multiple categories and some of them
    # are in list_of_cats than venue will appear in data that some times
    # so we will uniqify venues in data
    if len(list_of_cats) > 1:
        data = {v['pk']:v for v in data}.values()

    for restaurant in data:
        d = geopy_distance(currentPoint, restaurant['fields']['location']).kilometers
        restaurant['fields']['distance'] = round(d, 1)

        # Fancy splitting on POINT(lon, lat)
        lng = restaurant['fields']['location'].split()[1][1:]
        lat = restaurant['fields']['location'].split()[2][:-1]

        del restaurant['fields']['location']
        restaurant['fields']['lng'] = lng
        restaurant['fields']['lat'] = lat

        # Replace category ids with names
        cat_names = []
        for cat_id in restaurant['fields']['categories']:
            cat = models.Category.objects.get(id=cat_id)
            cat_names.append(cat.name)
        restaurant['fields']['categories'] = cat_names

    return data

def get_masjids(longitude, latitude, categories):
    '''
    Returns objects at given point that satisfy set of categories, 
    or all of them if categories is empty.
    input:
        str longitude
        str latitude
        list categories
    output:
        list of dicts
    '''
    currentPoint = geos.GEOSGeometry('POINT(%s %s)' %(longitude, latitude))
    distance_m = 15000
    list_of_cats = []
    for c in categories:
        list_of_cats.append(models.Category.objects.get(name=c))
    if list_of_cats:
        masjids = models.Masjid.gis.filter(
            location__distance_lte=(currentPoint, distance_m), 
            categories__in=list_of_cats
            )
    else:
        masjids = models.Masjid.gis.filter(location__distance_lte=(currentPoint, distance_m))

    # String based JSON
    data = serializers.serialize('json', masjids)
    # Actual JSON object to be edited
    data = json.loads(data)

    # if venue has multiple categories and some of them
    # are in list_of_cats than venue will appear in data that some times
    # so we will uniqify venues in data
    if len(list_of_cats) > 1:
        data = {v['pk']:v for v in data}.values()

    for masjid in data:
        d = geopy_distance(currentPoint, masjid['fields']['location']).kilometers
        masjid['fields']['distance'] = round(d, 1)

        # Fancy splitting on POINT(lon, lat)
        lng = masjid['fields']['location'].split()[1][1:]
        lat = masjid['fields']['location'].split()[2][:-1]

        del masjid['fields']['location']
        masjid['fields']['lng'] = lng
        masjid['fields']['lat'] = lat

        # Replace category ids with names
        cat_names = []
        for cat_id in masjid['fields']['categories']:
            cat = models.Category.objects.get(id=cat_id)
            cat_names.append(cat.name)
        masjid['fields']['categories'] = cat_names

    return data


def closest(request):
    if request.method == 'GET' and 'lat' in request.GET and 'lon' in request.GET:
        
        lat = float(request.GET['lat'])
        lon = float(request.GET['lon'])
        if 'category' in request.GET:
            categories = request.GET['category'].split('+')
        else:
            categories = []

        response_message = ''
        
        if request.GET.has_key('masjids'):
            venues = get_masjids(lon, lat, categories)
            if not venues:
                venues = get_masjids(lon, lat, categories=[])
                response_message = "No venues for this categories, here are some other ones you might like"
        else:
            venues = get_restaurants(lon, lat, categories)
            if not venues:
                venues = get_restaurants(lon, lat, categories=[])
                response_message = "No venues for this categories, here are some other ones you might like"

        return HttpResponse(
            json.dumps({
                "response":{
                    "total": len(venues),
                    "venues": sorted(venues, key = lambda venue: venue['fields']['distance']),
                    "message": response_message
                }
            }),  
            content_type='application/json'
        )
    else:
        return HttpResponse('Request method not correct')

@login_required
def comment(request, rest_pk):
    '''
    rest_pk must be valid one for existing restaurant or 
    ValueError will be raised on save() attempt in POST part. 
    '''
    context = {}

    if request.method == u'GET':
        try:
            filterargs = { 'venue_id': rest_pk, 'user': request.user }
            comment = models.Comment.objects.get(**filterargs)
            context['text'] = comment.text
            context['rating'] = comment.rating

        except ObjectDoesNotExist:
            pass


    if request.method == u'POST':
        try:
            rest = models.Restaurant.objects.get(id=rest_pk)
        except ObjectDoesNotExist:
            raise Http404

        filterargs = { 'venue_id': rest_pk, 'user': request.user }
        try:
            comment = models.Comment.objects.get(**filterargs)
        except ObjectDoesNotExist:
            comment = models.Comment(user = request.user, content_object = rest)
        comment.text = request.POST[u'comment']
        comment.rating = int(request.POST[u'rating'])
        comment.save()
        context['text'] = comment.text
        context['rating'] = comment.rating
        context['is_saved'] = True
        rest.update_avg_rating()

    context.update(csrf(request))
    return render_to_response('comment.html', context)

def show_all_comments(request, rest_pk):
    comments = models.Comment.objects.filter(venue_id=rest_pk)
    data = serializers.serialize('json', comments)
    data = json.loads(data)
    return HttpResponse(json.dumps({"response":{"total": len(data), "comments": data}}),  content_type='application/json')

@login_required
def tip(request, rest_pk):
    '''
    rest_pk must be valid one for existing restaurant or 
    ValueError will be raised on save() attempt in POST part. 
    '''
    context = {}

    if request.method == u'GET':
        try:
            filterargs = { 'venue_id': rest_pk, 'user': request.user }
            tip = models.Tip.objects.get(**filterargs)
            context['tip_text'] = tip.text
        except ObjectDoesNotExist:
            pass


    if request.method == u'POST':
        try:
            rest = models.Restaurant.objects.get(id=rest_pk)
        except ObjectDoesNotExist:
            raise Http404

        filterargs = { 'venue_id': rest_pk, 'user': request.user }
        try:
            tip = models.Tip.objects.get(**filterargs)
        except ObjectDoesNotExist:
            tip = models.Tip(user=request.user, content_object=rest)
        
        tip.text = request.POST[u'tip']
        tip.save()
        context['tip_text'] = tip.text
        context['is_saved'] = True

    context.update(csrf(request))
    return render_to_response('tip.html', context)

def show_all_tips(request, rest_pk):
    tips = models.Tip.objects.filter(venue_id=rest_pk)
    data = serializers.serialize('json', tips)
    data = json.loads(data)
    return HttpResponse(json.dumps({"response":{"total": len(data), "tips": data}}),  content_type='application/json')

@login_required
def update_restaurant(request, rest_pk):
    rest = models.Restaurant.objects.get(id=rest_pk)

    context = {'rest_pk': rest_pk}

    if request.method == 'POST':
        form = forms.RestaurantForm(request.POST, instance=rest) # A form bound to the POST data
        if form.is_valid():
            form.save()
            context['is_saved'] = True
        
        context['form'] = form
    
    else:
        context['form'] = forms.RestaurantForm(instance=rest)

    return render(request, 'update.html', context)

# @login_required
# def log_out(request):
#     logout(request)
#     return render(request, "comment.html")


@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.GET.get('access_token')
    user = request.backend.do_auth(request.GET.get('access_token'))
    if user:
        login(request, user)
        return HttpResponse(json.dumps({"success":True}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"success":False}), content_type='application/json')

