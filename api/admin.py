from django.contrib.gis import admin
from api import models

class RestaurantAdmin(admin.GeoModelAdmin):
    list_display = (
        'name', 
        'id', 
        'is_closed',
        'phone',
        'yelp_id',
        'yelp_url',
        'foursquare_id',
        'foursquare_url',
        'avg_rating'
    )
    readonly_fields = ('closed_reports_count',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'rating', 'short_text', 'user')
    fields = (('venue_name', 'user'), 'rating', 'text')
    readonly_fields = ('venue_name',)

class TipAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'text', 'user')
    fields = (('venue_name', 'user'), 'text')
    readonly_fields = ('venue_name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'venue_name',
        'report',
        'user',
        'moderator_note',
        'moderator_flag',
        'moderator'
    )

# Register your models here.
admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.Masjid, admin.GeoModelAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tip, TipAdmin)
admin.site.register(models.Report, ReportAdmin)