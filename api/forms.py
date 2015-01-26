from django import forms
from api import models

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = ['yelp_url', 'foursquare_url', 'phone', 'categories']

#TODO: write form for a Report
class ReportForm(forms.ModelForm):
    class Meta:
        model = models.Report
        fields = ['report', 'note']