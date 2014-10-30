from django.contrib.gis import admin
from api import models

class RestaurantInOneLine(admin.GeoModelAdmin):
    list_display = ('name', 'id', 'phone', 'yelp_id', 'yelp_url','foursquare_id','foursquare_url', 'avg_rating')

class CommentInOneLine(admin.ModelAdmin):
    fields = (('restaurant', 'user'), 'rating', 'text')
    list_display = ('restaurant', 'rating', 'short_text', 'user',)

# Register your models here.
admin.site.register(models.Restaurant, RestaurantInOneLine)
admin.site.register(models.Comment, CommentInOneLine)
admin.site.register(models.Category, admin.ModelAdmin)
admin.site.register(models.Tip, admin.ModelAdmin)