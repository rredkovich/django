from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models

# Create your models here.
class Restaurant(models.Model):
	name = models.CharField(max_length = 100)
	address = models.CharField(max_length = 150)
	phone = models.CharField(max_length = 12)
	cuisine = models.CharField(max_length = 50)
	eatingOptions = models.CharField(max_length = 50)
	location = gis_models.PointField(u'Latitude/Longitude', geography=True, blank=True, null=True)

	# Query Manager
	gis = gis_models.GeoManager()
	objects = models.Manager()

	def __unicode__(self):
		return self.name