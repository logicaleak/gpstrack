from gps3 import gps3
import datetime
import time
import MySQLdb

DB_IP = "192.168.1.100"
DB_USER = "root"
DB_PASS = ""
TABLE_NAME = "gps_konum"
DB_NAME = "plakadb"
WAIT_MS = 4


db = MySQLdb.connect(DB_IP,DB_USER,DB_PASS,DB_NAME)
cursor = db.cursor()

query = """
    update {tableName} set enlem={lat}, boylam={lon}
"""


def updateDatabase(lat, lon):
    now = datetime.datetime()
    formattedQuery = query.format(tableName=TABLE_NAME, lat=lat, lon=lon)
    try:
        cursor.execute(formattedQuery)
        db.commit()
    except:
        db.rollback()
    


def start_gps_app():
    while True:	
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

def trystuff():
    while True:
        time.sleep(2)
        print "hey"


def main():
    start_gps_app()
    

main()
