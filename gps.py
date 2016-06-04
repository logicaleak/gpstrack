import datetime
import time
import MySQLdb
import re
import os
import sys
import traceback

DB_IP = "localhost"
DB_USER = "root"
DB_PASS = "pass"
TABLE_NAME = "gps_konum"
LOG_TABLE_NAME = "gps_log"
DB_NAME = "plakadb"
WAIT_MS = 4


db = MySQLdb.connect(DB_IP,DB_USER,DB_PASS,DB_NAME)
cursor = db.cursor()

query = """
    update {tableName} set enlem={lat}, boylam={lon}, update_time=NOW()
"""
log_query = """
    insert into {tableName} (enlem, boylam, create_time) VALUES ({lat}, {lon}, NOW())
"""

def updateDatabase(lat, lon):
    formattedQuery = query.format(tableName=TABLE_NAME, lat=lat, lon=lon)
    try:
        cursor.execute(formattedQuery)
        db.commit()
    except:
        db.rollback()
    
def save_log(lat, lon):
    formattedQuery = log_query.format(tableName=LOG_TABLE_NAME, lat=lat, lon=lon)
    try:
        cursor.execute(formattedQuery)
        db.commit()
    except Exception as e:
        print traceback.format_exc()
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
                        save_log(fixedLat, fixedLon)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            continue
    


def main():
    gps_collect_function()
    

main()
