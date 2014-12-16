'''
Import to db venues from sqlite3.
'''
import sqlite3
from django.contrib.gis import geos
from api.models import Masjid

counter = 0

sq_conn = sqlite3.connect('masjid_05.12.db')
sq_curs = sq_conn.cursor()

for row in sq_curs.execute("SELECT * FROM Masjid;"):
    counter +=1
    masjid = Masjid(
        name = row[0],
        location = geos.GEOSGeometry('POINT(%s %s)' %(row[2], row[1]))
    )
    masjid.save()


print "Saved in db: ", counter
sq_conn.close()

# TABLE Masjid (
#     name text, 
#     latitude int, 
#     longitude int
# );

