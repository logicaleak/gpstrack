from gps3 import gps3
import datetime
import time
import MySQLdb

DB_IP = "localhost"
DB_USER = "root"
DB_PASS = "pass"
TABLE_NAME = "gps_konum"
LOG_TABLE_NAME = "GPS_log"
DB_NAME = "plakadb"
WAIT_MS = 4


db = MySQLdb.connect(DB_IP,DB_USER,DB_PASS,DB_NAME)
cursor = db.cursor()

query = """
    update {tableName} set enlem={lat}, boylam={lon}
"""
log_query = """
    insert into {tableName} (enlem, boylam, timestamp) VALUES ({lat}, {lon}, NOW())
"""

def updateDatabase(lat, lon):
    formattedQuery = query.format(tableName=TABLE_NAME, lat=lat, lon=lon)
    try:
        cursor.execute(formattedQuery)
        db.commit()
	print "success"
    except:
        db.rollback()
    
def save_log(lat, lon):
    formattedQuery = query.format(tableName=LOG_TABLE_NAME, lat=lat, lon=lon)
    try:
        cursor.execute(formattedQuery)
        db.commit()
    except:
        db.rollback()



def start_gps_app():
    gps_socket = gps3.GPSDSocket()
    gps_fix = gps3.Fix()
    gps_socket.connect()
    gps_socket.watch()
    while True:	
	print "a new loop"
	
        try:
            for new_data in gps_socket:
                if new_data:
		    print "Grabbed new data"
		    print new_data
                    gps_fix.refresh(new_data)
                    lat = gps_fix.TPV['lat']
                    lon = gps_fix.TPV['lon']
		    print "lat", lat, "lon", lon
                    #updateDatabase(lat, lon)
         	    #save_log(lat, lon)
                
        except:
            continue

def trystuff():
    while True:
        start_gps_app()
        


def main():
    start_gps_app()
    

main()
