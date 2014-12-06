'''
Import to db venues from sqlite3 only with categories,
which are in list categories_name.txt
'''
import sqlite3
from django.contrib.gis import geos
from api.models import Category, Restaurant

f = open('categories_name.txt','r')
cats = [c.replace("\n", "") for c in f.readlines()]
f.close()

valid_counter = 0
invalid_counter = 0

sq_conn = sqlite3.connect('restaurants_02.11.db')
sq_curs = sq_conn.cursor()

for row in sq_curs.execute("SELECT * FROM Restaurant;"):
    rest_cats = row[3].split(', ')
    rest_is_valid = False
    if len(rest_cats) == 0:
        rest_is_valid = True
    elif len(rest_cats) == 1:
        cat = rest_cats[0]
        if cat == "" or cat in cats:
            rest_is_valid = True
    else:
        for cat in rest_cats:
            if cat == "" or cat in cats:
                rest_is_valid = True
    # print row[2], " ", rest_is_valid
    if rest_is_valid:
        valid_counter +=1
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
        if len(rest_cats) == 1 and rest_cats[0] != '':
            print rest_cats[0]
            cat_in_db = Category.objects.get(name=rest_cats[0])
            rest.categories.add(cat_in_db)
            rest.save()
        elif len(rest_cats) > 1:
            for cat in rest_cats:
                print cat
                try:
                    cat_in_db = Category.objects.get(name=cat)
                    rest.categories.add(cat_in_db)
                    rest.save()
                except:
                    pass
    else:
        invalid_counter += 1

print "Saved in db: ", valid_counter
print "Have not applicable cusine: ", invalid_counter
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
