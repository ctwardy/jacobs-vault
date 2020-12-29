import sys
import os

import random

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import SQLContext
from pyspark.sql import Row

def createTrackData(shipRows):
    trackData={}
    for r in shipRows:
        mmsi=r[0]
        dt=r[1]
        lat=r[2]
        lon=r[3]
        coord=(lon,lat,0)
        if(mmsi not in trackData):
             trackData[mmsi]={"coord":[], "when":[]}
        trackData[mmsi]["coord"].extend([coord])
        trackData[mmsi]["when"].extend([str(dt)])
    return trackData

def createTrack(rows):
    rv=""
    for r in rows:
        rv=rv+"<Placemark>\n"
        dt=r[1]
        rv=rv + "  <TimeStamp>\n"
        rv=rv + "    <when>" + dt + "</when>\n"
        rv=rv + "  </TimeStamp>\n"
        lat=r[2]
        lon=r[3]
        rv=rv + "  <Point>\n"
        rv=rv + "    <coordinates>" + lon + "," + lat + "," + "0.0" + "</coordinates>\n"
        rv=rv + "  </Point>\n"
        rv=rv+"</Placemark>\n"
    return rv
    
def printKmlHeader():
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    print("<kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns:kml=\"http://www.opengis.net/kml/2.2\" xmlns:atom=\"http://www.w3.org/2005/Atom\">")
    print("<Document>")
    print("<name>" + "367331520" + "</name>")

def printKmlFooter():
    print("</Document>")
    print("</kml>")

def printKml(kml):
    printKmlHeader()
    print(kml)
    printKmlFooter()
