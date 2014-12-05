import psycopg2
import sqlite3
import csv


def makeQuery(row):
    #Now row here should be a list
    # query = "INSERT INTO api_restaurant(name, address, phone, cuisine, " + '"eatingOptions"' + ", location)" + " VALUES('" + row[0] + "', '" + row[1] + "', '" + row[2] + "', '" + row[3] + "', '" + row[4] + "', ST_Point(" + row[6] + ',' + row[5] + '))'
    query = "INSERT INTO api_restaurant(name, address, phone, cuisine, " + '"eatingOptions"' + ", yelp_id, foursquare_id, foursquare_url, location)" + " VALUES('" + row[0] + "', '" + row[1] + "', '" + row[2] + "', '" + row[3] + "', '" + row[4] + "', '" + row[5] + "', '" + row[6] + "', 'Null', ST_Point(" + row[8] + ',' + row[7] + '))'

    print query

    return query

# def insertData(connection, rowList):
#     cursor = connection.cursor()

#     for row in rowList:
#         print row
#         query = makeQuery(row)
#         cursor.execute(query)


if __name__ == '__main__':
    conn_ps = psycopg2.connect(dbname='restaurant0', host='localhost', user='muhammadali', password="tahity8^d0", port='5432')
    c_ps = conn_ps.cursor()

    conn_sq = sqlite3.connect('restaurant_fq.db')
    c_sq = conn_sq.connect()

    for row in c_sq.execute("SELECT * FROM Restaurant;"):
        query = makeQuery(list(row))
        c_ps.execute(query)

    conn_ps.commit()