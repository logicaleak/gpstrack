import datetime
import time
import MySQLdb
import os
import re

DB_IP = "192.168.1.100"
DB_USER = "root"
DB_PASS = ""
TABLE_NAME = "gps_konum"
DB_NAME = "plakadb"
WAIT_S = 3


db = MySQLdb.connect(DB_IP,DB_USER,DB_PASS,DB_NAME)
cursor = db.cursor()

query = """
    update {tableName} set enlem={lat}, boylam={lon} update_time=NOW()
"""


def updateDatabase(lat, lon):
    now = datetime.datetime()
    formattedQuery = query.format(tableName=TABLE_NAME, lat=lat, lon=lon)
    try:
        cursor.execute(formattedQuery)
        db.commit()
    except:
        db.rollback()
    


def gps_collect_function():
    while True:
        try:
            with open('/dev/ttyUSB0', 'r') as f: 
                while True:
                    line = f.readline()
                    splittedText = line.split(",")

                    if splittedText[0] == "$GPRMC":
                        latitudeUnfixed = splittedText[3]
                        longtitudeUnfixed = splittedText[5]
                        
                        #Fix latitudeUnfixed
                        fMinute = re.search("\d{2}\.\d+", latitudeUnfixed)
                        minutePart = fMinute.group(0)
                        fDegree = latitudeUnfixed.split(minutePart)[0]
                        fixedLat = float(minutePart) / 60 + float(fDegree)
                        
                        #Fix long
                        fMinute = re.search("\d{2}\.\d+", longtitudeUnfixed)
                        minutePart = fMinute.group(0)
                        fDegree = longtitudeUnfixed.split(minutePart)[0]
                        fixedLon = float(minutePart) / 60 + float(fDegree)
                        
                        updateDatabase(fixedLat, fixedLon)
		    time.sleep(WAIT_S)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            continue
            
           

def main():
    start_gps_app()
    

main()
