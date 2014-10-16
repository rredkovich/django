from django.contrib.gis import admin
from api import models

class CommentInOneLine(admin.ModelAdmin):
    fields = (('restaurant', 'user'), 'text')
    list_display = ('restaurant', 'short_text', 'user',)

# Register your models here.
admin.site.register(models.Restaurant, admin.GeoModelAdmin)
admin.site.register(models.Comment, CommentInOneLine)