from django import forms
from api import models

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = ['yelp_url', 'foursquare_url', 'phone', 'categories']
