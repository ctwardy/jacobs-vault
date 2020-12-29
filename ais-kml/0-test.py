import sys
import os

import random

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import SQLContext
from pyspark.sql import Row

#import pyCubes.FileUtils
#import pyCubes.GeoTagging
#import pyCubes.Shell
#import pyCubes.URLUtils

from simplekml import Kml, Model, AltitudeMode, Orientation, Scale

id=str(random.randint(11111,99999))

sparkConf=SparkConf().setAppName("Vault-AIS-" + id).set("spark.serializer", "org.apache.spark.serializer.KryoSerializer").set("spark.sql.broadcastTimeout", "9000").set("spark.kryoserializer.buffer.max", "1gb").set("spark.driver.maxResultSize","2g")


#sc = SparkContext("yarn", "Vault-AIS-" + id)
sc = SparkContext("yarn", conf=sparkConf)


sqlContext = SQLContext(sc)
sparkSession = SparkSession(sc)

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

#kml=createTrack(tblData)
#printKnl(kml)

tblAis=sparkSession.table("vault.ais_raw").filter("BaseDateTime like '2017%'")
tblShip=tblAis.sort("mmsi","BaseDateTime")
tblData=tblShip.collect()

shipTracks=createTrackData(tblData)

#for shipTrack in shipTracks:
#    print(shipTrack, len(shipTracks[shipTrack]["when"]))
#quit()

kml = Kml(name='AISSample-' + id, open=1)

# Create the model
model_ship = Model(altitudemode=AltitudeMode.clamptoground,
                           orientation=Orientation(heading=0.0),
                           scale=Scale(x=1.0, y=1.0, z=1.0))

for shipTrack in shipTracks:
# Create the track
    trk = kml.newgxtrack(name="AIS-" + shipTrack, altitudemode=AltitudeMode.clamptoground,description=shipTrack)

    # Attach the model to the track
    trk.model = model_ship
    #trk.model.link.href = car_dae

    # Add all the information to the track
    trk.newwhen(shipTracks[shipTrack]["when"])
    trk.newgxcoord(shipTracks[shipTrack]["coord"])

    # Turn-off default icon and text and hide the linestring
    #trk.iconstyle.icon.href = ""
    #trk.labelstyle.scale = 0
    #trk.linestyle.width = 0

# Saving
filename="aistest2-" + id
kml.save(filename + ".kml")
kml.savekmz(filename + ".kmz") # uncomment to save to kmz
#print kml.kml() # uncomment to see the kml printed to screen
