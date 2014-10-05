from django.contrib.gis import admin
from api import models

# Register your models here.
admin.site.register(models.Restaurant, admin.GeoModelAdmin)
admin.site.register(models.Comment)