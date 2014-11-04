from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, URLValidator

import datetime


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 150)
    phone = models.CharField(
        max_length = 12, 
        blank=True, 
        validators=[
            RegexValidator(
                regex=r'^[0-9]+$', 
                message='Only digits allowed'
                )
            ]
    )
    cuisine = models.CharField(max_length = 50)
    eatingOptions = models.CharField(max_length = 50)
    location = gis_models.PointField(
        u'Latitude/Longitude', 
        geography=True, 
        blank=True, 
        null=True
    )
    yelp_id = models.CharField(max_length=255, blank=True)
    yelp_url = models.CharField(max_length=255, blank=True, validators=[URLValidator()])
    foursquare_id = models.CharField(max_length=100, blank=True)
    foursquare_url = models.CharField(max_length=255, blank=True, validators=[URLValidator()])

    categories = models.ManyToManyField(Category, null=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    # User can make changes in this model,
    # look at views.update_restaurant()
    modified_by = models.ForeignKey(User, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True)

    # Query Manager
    gis = gis_models.GeoManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.name

    def update_avg_rating(self):
        self_comments = Comment.objects.filter(restaurant = self)
        num_of_comments = float(len(self_comments))
        if num_of_comments == 0.0:
            return
        avg_rating = 0.0
        for comment in self_comments:
            avg_rating += comment.rating / num_of_comments
        self.avg_rating = avg_rating
        self.save()


class Comment(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    rating = models.IntegerField(null=True, blank=True)
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