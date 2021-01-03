
from datetime import datetime
from flask import Flask
from flask import request

from flask import send_file, render_template, render_template_string, Markup

import json

try:
    # restplus is dead: https://github.com/noirbizarre/flask-restplus/issues/770
    from flask_restx import Resource, Api
    from flask_restx import reqparse
except ImportError:
    try:
        from flask_restplus import Resource, Api
    except ImportError:

        import werkzeug
        werkzeug.cached_property = werkzeug.utils.cached_property
        from flask_restplus import Resource, Api
        from flask_restplus import reqparse
from markupsafe import escape
import json

app = Flask(__name__)
api = Api(app)

# e.g.: http://127.0.0.1:5000/test?ts=1467244800&lat=45.0&lon=-176.0

@api.route('/test')
class TestService(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ts', type=int, help='unix epoch seconds')
        parser.add_argument('lat', type=float, help='datetime in unix time format')
        parser.add_argument('lon', type=float, help='datetime in unix time format')
        args = parser.parse_args()

        dt = datetime.fromtimestamp(args["ts"])
        result = {"response" : "HelloWorld"}
        return result

@api.route('/get_image')
class ImageService(Resource):
    def get(self):
        icon1="icons/circle-xl.png"
        return send_file(icon1, mimetype='image/png')


def calculateVisibleData(visibleData):
    hits=visibleData["hit"]
    altitude=visibleData["altitude"]
    miss=visibleData["miss"]
    days=visibleData["days"]
    azimuth=visibleData["azimuth"]

    sats={}
    for h in hits:
        if(not h in sats):
            sats[h]={"hits":"", "altitude":"", "miss":"", "days":"", "azimuth":""}
        sats[h]["hits"]=str(hits[h])
    for h in altitude:
        sats[h]["altitude"]=str(altitude[h])
    for h in days:
        sats[h]["days"]=str(days[h])
    for h in azimuth:
        sats[h]["azimuth"]=str(azimuth[h])
       
    return sats

def createHitMissSummaryTable(hitmissData):
    rv=     "<div id='hitMissContent'>"
    rv=rv+  "<table class='hitMissTable' border=1>"
    rv=rv+  "<tr><td>Quality</td><td>Count</td></tr>"
    rv=rv + "<tr><td>Excellent</td><td>" + str(hitmissData["0"]["Excellent"]) + "</td></tr>"
    rv=rv + "<tr><td>Good</td><td>" + str(hitmissData["0"]["Good"]) + "</td></tr>"
    rv=rv + "<tr><td>Stale</td><td>" + str(hitmissData["0"]["Stale"]) + "</td></tr>"
    rv=rv + "<tr><td>Poor</td><td>" + str(hitmissData["0"]["Poor"]) + "</td></tr>"

    rv=rv+"</table>"
    rv=rv+ "</div>"
    return rv

        
@app.route("/html")
def index():

#this top section can be replaced with theinputs/outputs of the existing eval function
    mmsi="0123456789"
    lat="32.3432423"
    lon="45.1231231"
    dt="34873482"


    rawJson=open("sample1.json",'r').read().strip()
    jsonData=json.loads(rawJson)
    hitData=json.loads(jsonData["response"])
#tohere


    visibleData=hitData["visible"]
    hitmissdata=hitData["hitmiss"]

    visibleArray=calculateVisibleData(visibleData)

    htmlcontent=""

    htmlcontent=htmlcontent+createHitMissSummaryTable(hitmissdata)

    visibleContent="<div id='visibleContent'>"
    visibleContent=visibleContent+ "<table border=1>"
    vissibleRow="<tr>"
    vissibleRow=vissibleRow+"<td><span class='visibleRowItem'>Sat</span></td>"
    vissibleRow=vissibleRow+"<td><span class='visibleRowItem'>Hits</span></td>"
    vissibleRow=vissibleRow+"<td><span class='visibleRowItem'>Altitude</span></td>"
    vissibleRow=vissibleRow+"<td><span class='visibleRowItem'>Days</span></td>"
    vissibleRow=vissibleRow+"<td><span class='visibleRowItem'>Azimuth</span></td>"
    vissibleRow=vissibleRow+"</tr>"
    visibleContent=visibleContent+vissibleRow

    for x in visibleArray:
        vissibleRow="<tr class='visibleRow'>"
        vissibleRow=vissibleRow+"<td><span class='visibleRowItem'>" + x + "</span></td>"
        vissibleRow=vissibleRow+"<td><span class='visibleRowItem'>" + visibleArray[x]["hits"] + "</span></td>"
        vissibleRow=vissibleRow+"<td><span class='visibleRowItem'>" + visibleArray[x]["altitude"] + "</span></td>"
        vissibleRow=vissibleRow+"<td><span class='visibleRowItem'>" + visibleArray[x]["days"] + "</span></td>"
        vissibleRow=vissibleRow+"<td><span class='visibleRowItem'>" + visibleArray[x]["azimuth"] + "</span></td>"
        vissibleRow=vissibleRow+"</tr>"
        visibleContent=visibleContent+vissibleRow  
    visibleContent=visibleContent+"</table>"
    htmlcontent=htmlcontent+visibleContent
    

    templateFile="hittesttemplate.html"
    rendered = render_template(templateFile, title='MMSI Hits and Misses', mmsi=mmsi, timestamp=dt, lat=lat, lon=lon, content=Markup(htmlcontent))
    return(rendered)
