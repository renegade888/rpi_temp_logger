#!/usr/bin/env python

import sqlite3
import sys
import platform
from collections import namedtuple
import cgi
import cgitb

SensorRecord = namedtuple('sensor','sensor_name, sensor_id')
SensorDataRecord = namedtuple('sensor_data','sensorid_id,timestamp,value')
# global variables
dbname='/var/www/tmplog/tempdb2.db'

# print the HTTP header
def printHTTPheader():
    print "Content-type: text/html\n\n"

# print the HTML head section
# arguments are the page title and the table for the chart
def printHTMLHead(title, table):
    print "<head>"
    print "    <title>"
    print title
    print "    </title>"
    print_graph_script(table)
    print "</head>"

#Get the number of sensors
def getSensorCount():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("select count(DISTINCT sensor.sensor_id) from sensor;")
    rows=curs.fetchone()
    conn.close()
    return int(format((rows[0])))

#get Sensor timestamp and value based on device ID 
def getSensorData(interval):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    if interval is None:
        #uptimize - we dont need all data
        curs.execute("SELECT sensor_data.sensor_id, timestamp, value FROM sensor_data WHERE timestamp>=datetime('now','-1 hours','+2 hours')")
    else:
        curs.execute("SELECT sensor_data.sensor_id, timestamp, value FROM sensor_data WHERE timestamp>=datetime('now','-{0} hours','+2 hours')".format(interval))
    return map(SensorDataRecord._make,curs.fetchall())

#return a list of sensorIds
def getSensorIds():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    sensorIdRow=curs.execute("select DISTINCT sensor.sensor_id, sensor.sensor_name from sensor;")
    rows=curs.fetchall()
    conn.close()
    devicedata =[]
    for row in rows:
        rowdata =[]
        rowdata.append(str(row[0]))
        rowdata.append(str(row[1]))
        devicedata.append(rowdata)
    return devicedata

#Creates the first item in data array based on #sensors
def getBaseTable():
    baseTable = "['Time',"
    sensorids = getSensorIds()
    for sensor in sensorids[:-1]:#every sensor except last sensor
        rowstr="'{0}',".format(str(sensor[1]))
        baseTable += rowstr
    baseTable+="'{0}'],\n".format(str(sensorids[-1][1]))#last sensor (-1) #sensorname[1]
    return baseTable
# TODO - Make this thing dynamic. 
# To more sensors added, add them in in line 83+84+85
# convert rows from database into a javascript table
def createMultiTable(interval):
    sensorCount = getSensorCount()
    dataTable=getBaseTable()
    devicedata = getSensorData(interval)
    dataTable+="['{0}',{1},".format(devicedata[0].timestamp,devicedata[0].value)
    cnt = 1
    for data in devicedata[1:-1]:
        if cnt % sensorCount is 0:
            dataTable+="],\n["
            dataTable+="'{0}',".format(data.timestamp)
            cnt = 0
        if cnt is sensorCount:
            dataTable+="]{0}".format(data.value)
            cnt = 0
        if cnt is sensorCount -1:
            dataTable+="{0}".format(data.value)
        elif cnt is not sensorCount:
            dataTable+="{0},".format(data.value)
        cnt += 1
    dataTable+="'{0}']".format(devicedata[-1].value)
    return dataTable

# print the javascript to generate the chart
# pass the table generated from the database info
def print_graph_script(table):

    # google chart snippet
    chart_code="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          %s
        ]);

        var options = {
          title: 'Temperature',
          curveType: 'function'

        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>"""
    print chart_code % (table)

# print the div that contains the graph
def show_graph():
    print "<h2>Temperature Chart</h2>"
    print '<div id="chart_div" style="width: 1000px; height: 500px;"></div>'

# connect to the db and show some stats
# argument option is the number of hours
def show_stats(interval):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if not interval:
        interval = str(24)

    curs.execute("SELECT timestamp,max(value) FROM sensor_data WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now','+2 hour')" % interval)
    rowmax=curs.fetchone()
    rowstrmax="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmax[0]),str(rowmax[1]))

    curs.execute("SELECT timestamp,min(value) FROM sensor_data WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now','+2 hour')" % interval)
    rowmin=curs.fetchone()
    rowstrmin="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmin[0]),str(rowmin[1]))

    curs.execute("SELECT avg(value) FROM sensor_data WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now','+2 hour')" % interval)
    rowavg=curs.fetchone()

    print "<hr>"
    print "<h2>Minumum temperature&nbsp</h2>"
    print rowstrmin
    print "<h2>Maximum temperature</h2>"
    print rowstrmax
    print "<h2>Average temperature</h2>"
    print "%.3f" % rowavg+"C"

    print "<hr>"

    print "<h2>In the last hour:</h2>"
    print "<table>"
    print "<tr><td><strong>Date/Time</strong></td><td><strong>Temperature</strong></td><td><strong>Device</strong></td></tr>"

    rows=curs.execute("SELECT timestamp,value,sensor_id FROM sensor_data WHERE timestamp>datetime('now','+1 hour') AND timestamp<=datetime('now','+2 hour')")
    for row in rows:
        rowstr="<tr><td>{0}&emsp;&emsp;</td><td>{1}C</td><td>{2}</td></tr>".format(str(row[0]),str(row[1]),str(row[2]))
        print rowstr
    print "</table>"
    print "<hr>"
    conn.close()

def print_time_selector(option):
    print """<form action="/index.py" method="POST">
        Show the temperature logs for  
        <select name="timeinterval">"""

    if option is not None:
        if option == "1":
            print "<option value=\"1\" selected=\"selected\">the last 1 hour</option>"
        else:
            print "<option value=\"1\">the last 1 hour</option>"
        if option == "6":
            print "<option value=\"6\" selected=\"selected\">the last 6 hours</option>"
        else:
            print "<option value=\"6\">the last 6 hours</option>"

        if option == "12":
            print "<option value=\"12\" selected=\"selected\">the last 12 hours</option>"
        else:
            print "<option value=\"12\">the last 12 hours</option>"

        if option == "24":
            print "<option value=\"24\" selected=\"selected\">the last 24 hours</option>"
        else:
            print "<option value=\"24\">the last 24 hours</option>"
        if option == "168":
            print "<option value=\"168\" selected=\"selected\">the last week</option>"
        else:
            print "<option value=\"168\">the last week</option>"
    else:
        print """<option value="1">the last 1 hour</option>
            <option value="6">the last 6 hours</option>
            <option value="12">the last 12 hours</option>
            <option value="24" selected="selected">the last 24 hours</option>
            <option value="168" selected="selected">the last week</option>"""

    print """        </select>
        <input type="submit" value="Display">
    </form>"""


# check that the option is valid
# and not an SQL injection
def validate_input(option_str):
    # check that the option string represents a number
    if option_str.isalnum():
        # check that the option is within a specific range
        if int(option_str) > 0 and int(option_str) <= 168:
            return option_str
        else:
            return None
    else:
        return None


#return the option passed to the script
def getTimeInterval():
    form=cgi.FieldStorage()
    if "timeinterval" in form:
        option = form["timeinterval"].value
        return validate_input (option)
    else:
        return None
# main function
# This is where the program starts 
def main():
    cgitb.enable()
    # get options that may have been passed to this script
    interval=getTimeInterval()
    if not interval:
        interval= str(1) #24 hour std interval

    printHTTPheader()
    if getSensorCount() is 0:
        print "No data found"
        return
    else:
        table = createMultiTable(interval)
    # print the head section including the table
    # used by the javascript for the chart
    printHTMLHead("Raspberry Pi Temperature Logger", table)
    # print the page body
    print "<body>"
    print "<h1>Temperature Logger</h1>"
    print "<hr>"
    print_time_selector(interval)
    show_graph()
    #show_stats(interval)
    print "</body>"
    print "</html>"
    sys.stdout.flush()

if __name__=="__main__":
    main()
