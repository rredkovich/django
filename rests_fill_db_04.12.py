'''
Import to db venues from sqlite3 with categories,
if category not in list categories_name.txt, adds without one.
'''

import sqlite3
from django.contrib.gis import geos
from api.models import Category, Restaurant

f = open('categories_name.txt','r')
cats = [c.replace("\n", "") for c in f.readlines()]
f.close()

counter = 0

sq_conn = sqlite3.connect('restaurants_02.11.db')
sq_curs = sq_conn.cursor()

for row in sq_curs.execute("SELECT * FROM Restaurant;"):
    rest_cats = row[3].split(', ')
    counter +=1
    rest = Restaurant(
        name = row[0],
        address = row[1],
        phone = row[2].replace(" ", "") or '',
        cuisine = row[3],
        eatingOptions = row[4],
        location = geos.GEOSGeometry('POINT(%s %s)' %(row[10], row[9])),
        yelp_id = row[5] or '',
        yelp_url = row[6] or '',
        foursquare_id = row[7] or '',
        foursquare_url = row[8] or '',
    )
    rest.save()
    for cat in rest_cats:
        try:
            cat_in_db = Category.objects.get(name=cat)
            rest.categories.add(cat_in_db)
            rest.save()
        except:
            pass

print "Saved in db: ", counter
sq_conn.close()

# TABLE Restaurant (
#     0name text, 
#     1address text, 
#     2phone int,
#     3cuisine text, 
#     4eating_options text, 
#     5yelp_id text, 
#     6yelp_url text, 
#     7fq_id text,  
#     8fq_url text, 
#     9latitude int, 
#     10longitude int
# );
