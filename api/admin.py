from django.contrib.gis import admin
from api import models

class RestaurantInOneLine(admin.GeoModelAdmin):
    list_display = ('name', 'id', 'phone', 'yelp_id', 'yelp_url','foursquare_id','foursquare_url', 'avg_rating')

class CommentInOneLine(admin.ModelAdmin):
    fields = (('restaurant', 'user'), 'rating', 'text')
    list_display = ('restaurant', 'rating', 'short_text', 'user')

class TipInOneLine(admin.ModelAdmin):
    fields = (('restaurant', 'user'), 'text')
    list_display = ('restaurant', 'text', 'user')

class CategoryInOneLine(admin.ModelAdmin):
    list_display = ('name', 'id')

# Register your models here.
admin.site.register(models.Restaurant, RestaurantInOneLine)
admin.site.register(models.Comment, CommentInOneLine)
admin.site.register(models.Category, CategoryInOneLine)
admin.site.register(models.Tip, TipInOneLine)