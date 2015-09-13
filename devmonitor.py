#!/usr/bin/env python

import sqlite3
import glob
import random
import commands

# global variables
dbname='/var/www/tmplog/tempdb2.db'

# store the temperature in the database
def log_temperature(iD, temp):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    insertDeviceQuery = "INSERT OR IGNORE INTO sensor (sensor_id) VALUES('"+str(iD)+"');"
    curs.execute(insertDeviceQuery);
    insertDataQuery = "INSERT INTO sensor_data (sensor_id,value) VALUES('"+str(iD)+"','"+str(temp)+"');"
    curs.execute(insertDataQuery);
    # commit the changes
    conn.commit()
    conn.close()

# main function
# This is where the program starts 
def main():
    devicelist = ['device1','device2',"device321"]
    if devicelist=='':
        # no devices
        return None
    else:
        for device in devicelist:
            temperature = random.uniform(15.0,25.0)
            deviceid = device
            print temperature
            print deviceid
            log_temperature(deviceid, temperature)
if __name__=="__main__":
    main()
