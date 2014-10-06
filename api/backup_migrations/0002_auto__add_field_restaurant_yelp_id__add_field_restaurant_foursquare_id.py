# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Restaurant.yelp_id'
        db.add_column(u'api_restaurant', 'yelp_id',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'Restaurant.foursquare_id'
        db.add_column(u'api_restaurant', 'foursquare_id',
                      self.gf('django.db.models.fields.BigIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Restaurant.foursquare_url'
        db.add_column(u'api_restaurant', 'foursquare_url',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Restaurant.yelp_id'
        db.delete_column(u'api_restaurant', 'yelp_id')

        # Deleting field 'Restaurant.foursquare_id'
        db.delete_column(u'api_restaurant', 'foursquare_id')

        # Deleting field 'Restaurant.foursquare_url'
        db.delete_column(u'api_restaurant', 'foursquare_url')


    models = {
        u'api.restaurant': {
            'Meta': {'object_name': 'Restaurant'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'cuisine': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'eatingOptions': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'foursquare_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'foursquare_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'yelp_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['api']