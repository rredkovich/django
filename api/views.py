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

# from django.contrib.auth import logout

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
        restaurant['fields']['distance'] = round(d, 2)

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
    

# "No restaurants for this categories, here are some other ones you might like"

def closest(request):
    if request.method == 'GET' and 'lat' in request.GET and 'lon' in request.GET:
        
        lat = float(request.GET['lat'])
        lon = float(request.GET['lon'])
        if 'category' in request.GET:
            categories = request.GET['category'].split('+')
        else:
            categories = []

        response_message = ''
        restaurants = get_restaurants(lon, lat, categories)
        
        if not restaurants:
            restaurants = get_restaurants(lon, lat, categories=[])
            response_message = "No restaurants for this categories, here are some other ones you might like"


        return HttpResponse(
            json.dumps({
                "response":{
                    "total": len(restaurants),
                    "venues": sorted(restaurants, key = lambda rest: rest['fields']['distance']),
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
    try:
        rest = models.Restaurant.objects.get(id=rest_pk)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == u'GET':
        try:
            filterargs = { 'restaurant': rest, 'user': request.user }
            comment = models.Comment.objects.get(**filterargs)
            context['text'] = comment.text
            context['rating'] = comment.rating

        except ObjectDoesNotExist:
            pass


    if request.method == u'POST':
        filterargs = { 'restaurant': rest, 'user': request.user }
        comment, is_created = models.Comment.objects.get_or_create(**filterargs)
        comment.text = request.POST[u'comment']
        comment.rating = int(request.POST[u'rating'])
        if is_created:
            comment.user = request.user
            comment.restaurant = rest
        comment.save()
        context['text'] = comment.text
        context['rating'] = comment.rating
        context['is_saved'] = True
        rest.update_avg_rating()

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
    return HttpResponse(json.dumps({"response":{"total": len(data), "comments": data}}),  content_type='application/json')

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
        context['is_saved'] = True

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

