from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models
from django.contrib.auth.models import User
import datetime

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 150)
    phone = models.CharField(max_length = 12)
    cuisine = models.CharField(max_length = 50)
    eatingOptions = models.CharField(max_length = 50)
    location = gis_models.PointField(u'Latitude/Longitude', geography=True, blank=True, null=True)
    yelp_id = models.CharField(max_length=255, blank=True)
    yelp_url = models.CharField(max_length=255, blank=True)
    foursquare_id = models.CharField(max_length=100, blank=True)
    foursquare_url = models.CharField(max_length=255, blank=True)

    categories = models.ManyToManyField(Category)

    # Query Manager
    gis = gis_models.GeoManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.name

class Comment(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return self.text[:25]

    def short_text(self):
        return self.__unicode__()

class Tip(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    text = models.TextField(max_length=200, blank=True)

    def __unicode__(self):
        return self.text[:25]