#!/usr/bin/env python

import sqlite3
import os
import glob
import commands

# global variables
speriod=(15*60)-1
dbname='/var/www/tmplog/tempdb2.db'



# store the temperature in the database
def log_temperature(iD, temp):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    insertDataQuery = "INSERT INTO sensor_data (sensor_id,value) VALUES('"+str(iD)+"','"+str(temp)+"');"
    curs.execute(insertDataQuery);
    # commit the changes
    conn.commit()
    conn.close()

# display the contents of the database
def display_data(iD):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    getSensorDataQuery = "SELECT * FROM sensor_data WHERE sensor_id =?"
    for row in curs.execute(getSensorDataQuery, [iD]):
        print str(row[1])+"	"+str(row[3])

    conn.close()

# get temperature
# returns None on error, or the temperature as a float
def get_temp(devicefile):

    try:
        fileobj = open(devicefile,'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        return None

    # get the status from the end of line 1 
    status = lines[0][-4:-1]

    # is the status is ok, get the temperature from line 2
    if status=="YES":
        print status
        tempstr= lines[1][-6:-1]
        tempvalue=float(tempstr)/1000
        print tempvalue
        return tempvalue
    else:
        print "There was an error."
        return None

# main function
# This is where the program starts 
def main():

    # enable kernel modules
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')

    # search for a device file that starts with 28
    deviceDir = '/sys/bus/w1/devices/'
    devicelist = glob.glob(deviceDir + '28*')

    if devicelist=='':
        # no devices
        return None
    else:
        # append /w1slave to the device file
        for w1devicefile in devicelist:
            w1devicefile = w1devicefile + '/w1_slave'
            # get the temperature from the device file
            temperature = get_temp(w1devicefile)
            while temperature == None:
                temperature = get_temp(w1devicefile)

            deviceid = w1devicefile.split("/")[5]
            # Store the temperature in the database
            log_temperature(deviceid, temperature)

if __name__=="__main__":
    main()
