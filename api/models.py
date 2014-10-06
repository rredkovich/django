from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models
# from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Restaurant(models.Model):
	name = models.CharField(max_length = 100)
	address = models.CharField(max_length = 150)
	phone = models.CharField(max_length = 12)
	cuisine = models.CharField(max_length = 50)
	eatingOptions = models.CharField(max_length = 50)
	location = gis_models.PointField(u'Latitude/Longitude', geography=True, blank=True, null=True)
	yelp_id = models.CharField(max_length=255,null=True)
	foursquare_id = models.CharField(max_length=100, null=True)
	foursquare_url = models.CharField(max_length=255,null=True)

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
	text = models.TextField(max_length=255)
