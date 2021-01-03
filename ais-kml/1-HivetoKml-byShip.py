import sys
import os
import random
import datetime
from datetime import timedelta

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import SQLContext
from pyspark.sql import Row

from simplekml import Kml, Model, AltitudeMode, Orientation, Scale, Style

id=str(random.randint(11111,99999))

colidx_mmsi=0
colidx_datetime=2
colidx_vesselname=10
colidx_lat=23
colidx_lon=26
colidx_cnt=27

hittestserver="http://10.121.20.10:5000"

def randomColor():
    r = lambda: random.randint(0,255)
    color = "%06x" % random.randint(0, 0xFFFFFF)
    return color

def totimestamp(dt):
    epoch=datetime.datetime(1970,1,1)
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6 

def createDescriptionTemplate():
    rv="<![CDATA[MMSI: {mmsi}\n<br />"
    rv=rv + "Dt: {datetime}\n\n<br />"
    rv=rv + "Hits: {count}<br />"
    rv=rv + "<a href='" + hittestserver + "/html?ts={timestamp}&lat={lat}&lon={lon}&mmsi={mmsi}'>Satellite Lookup</a><br />"
#    rv=rv + "<img style='max-width:100px;' src='" + hittestserver + "/eval?ts={timestamp}&lat={lat}&lon={lon}&mmsi={mmsi}'>]]>"
    return rv

def getStyle(color):
    shared_style_common=Style()
    shared_style_common.labelstyle.color = "66ffffff"
    shared_style_common.labelstyle.scale = 0.1
    shared_style_common.iconstyle.color = "88ff0000"
    shared_style_common.iconstyle.scale = 0.25
    shared_style_common.linestyle.width=0.15
    shared_style_common.linestyle.color="66" + color
    return shared_style_common

def createShipKml(mmsi, vesselname, shipRows):
    kml = Kml(name='mmsi-' + mmsi, open=1)
    model_ship = Model(altitudemode=AltitudeMode.clamptoground,
                           orientation=Orientation(heading=0.0),
                           scale=Scale(x=1.0, y=1.0, z=1.0))

    container=kml.newdocument(name=mmsi)
    mmsi_color=randomColor()
    kml.style=getStyle("ffffff")
    container.style=getStyle("ffffff")

    descriptionTemplate=createDescriptionTemplate()

    for shipRow in shipRows:
        mmsi=shipRow[colidx_mmsi]
        dt=shipRow[colidx_datetime]
        lat=shipRow[colidx_lat]
        lon=shipRow[colidx_lon]
        cnt=int(shipRow[colidx_cnt])

        dTime=datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
        dTime2=dTime+timedelta(hours=1)
        dtimeEnd=dTime2.replace(microsecond=0).isoformat()
        ts=int(totimestamp(dTime))

        coords=[(lon, lat)]

        description=descriptionTemplate.replace("{datetime}",dt).replace("{lat}",str(lat)).replace("{lon}",str(lon)).replace("{mmsi}",mmsi).replace("{count}",str(cnt)).replace("{timestamp}",str(ts))

        pnt=container.newpoint(name=mmsi, description="description", coords=coords)
        pnt.description=description
#        pnt.snippet.content="snippet content"
        pnt.timestamp.when = dt
#        pnt.timespan.begin = dt
#        pnt.timespan.end = dtimeEnd
#        pnt.timespan.end = nextTimes[dt]
#        pnt.style=shared_style_common
          
    # Saving
    filename="mmsi-" 
    if(vesselname!=""):
        filename=filename + vesselname + "-"
    filename=filename + mmsi


    kml.savekmz(filename + ".kmz")
    return (filename, kml)


sparkConf=SparkConf().setAppName("Vault-AIS-" + id).set("spark.serializer", "org.apache.spark.serializer.KryoSerializer").set("spark.sql.broadcastTimeout", "9000").set("spark.kryoserializer.buffer.max", "1gb").set("spark.driver.maxResultSize","2g")

#sc = SparkContext("yarn", "Vault-AIS-" + id)
sc = SparkContext("yarn", conf=sparkConf)
sqlContext = SQLContext(sc)
sparkSession = SparkSession(sc)
tblAis=sparkSession.table("af_vault.ais_agg_stats_hourly").filter("datetime like '2017%'") 

tblFilterTable=sqlContext.sql("select mmsi as mmsi2, sum(cnt) as c from af_vault.ais_agg_stats_hourly where datetime like '2017%' group by mmsi2 order by c desc limit 1000").select("mmsi2")
tblAis = tblAis.join(tblFilterTable,tblAis.mmsi==tblFilterTable.mmsi2, how="inner")

tblShip=tblAis.sort("mmsi","datetime")

tblData=tblShip.collect()

kmls=[]
mmsi=""
last_mmsi=""
shipRows=[]
for d in tblData:
    mmsi=d[colidx_mmsi]
    vesselname=d[colidx_vesselname].strip().replace(" ","-").replace("/","").replace("\\","")
    if(mmsi!=last_mmsi):
        if(len(shipRows)>0):
            filename, kml=createShipKml(last_mmsi,vesselname, shipRows)
            kmls.extend([(filename, kml)])
        shipRows=[]
        last_mmsi=mmsi
    shipRows.extend([d])
filename, kml=createShipKml(last_mmsi,vesselname, shipRows)     
kmls.extend([(filename, kml)])


kml=Kml(name="mmsi-Index", open=1)
for x in kmls:
    (filename,kml2)=x
    if(filename!=""):
        lnk=kml.newnetworklink(name=filename)
        lnk.link.href = "/kml/placemarks/" + filename + ".kmz"
#    lnk.link.viewrefreshmode = simplekml.ViewRefreshMode.onrequest
kml.save("index.kml")


