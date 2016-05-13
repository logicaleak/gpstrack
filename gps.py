from gps3 import gps3
import datetime
import time
import MySQLdb

DB_IP = ""
DB_USER = ""
DB_PASS = ""
tableName = "table"
dbName = "dbName"
WAIT_MS = 4000


db = MySQLdb.connect(DB_IP,DB_USER,DB_PASS,dbName)
cursor = db.cursor()

query = """
    update {tableName} set lat={lat}, lon={lon}
"""


def updateDatabase(lat, lon):
    now = datetime.datetime()
    formattedQuery = query.format(lat=lat, lon=lon)
    try:
        cursor.execute(formattedQuery)
        db.commit()
    except:
        db.rollback()
    


while true:
    gps_socket = gps3.GPSDSocket()
    gps_fix = gps3.Fix()
    gps_socket.connect()
    gps_socket.watch()
    try:
        for new_data in gps_socket:
            if new_data:
                gps_fix.refresh(new_data)
                lat = gps_fix.TPV['lat']
                lon = gps_fix.TPV['lon']
                updateDatabase(lat, lon)
            time.sleep(WAIT_MS)
    except:
        continue
