
from datetime import datetime
from flask import Flask
from flask import request
from flask import send_file, render_template, render_template_string, Markup
import json

class HTMLConvert:

    def calculateVisibleData(self, visibleData):
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

    def createHitMissSummaryContent(self, hitmissData):
        rv=""
        rv=rv + "<div class='hitMissItem'><div class='hitMissLabel'>Excellent:</div><div class='hitMissValue'>" +  str(hitmissData["0"]["Excellent"]) + "</div></div>"
        rv=rv + "<div class='hitMissItem'><div class='hitMissLabel'>Good:</div><div class='hitMissValue'>" +  str(hitmissData["0"]["Good"]) + "</div></div>"
        rv=rv + "<div class='hitMissItem'><div class='hitMissLabel'>Stale:</div><div class='hitMissValue'>" +  str(hitmissData["0"]["Stale"]) + "</div></div>"
        rv=rv + "<div class='hitMissItem'><div class='hitMissLabel'>Poor:</div><div class='hitMissValue'>" +  str(hitmissData["0"]["Poor"]) + "</div></div>"
        return rv


    def createVisibleSummaryContent(self, visibleArray):
        rv=""
        for x in visibleArray:
            visibleRow="<tr class='visibleRow'>"
            visibleRow=visibleRow + "<td><span class='visibleRowItem'>" + x + "</span></td>"
            visibleRow=visibleRow + "<td><span class='visibleRowItem'>" + visibleArray[x]["hits"] + "</span></td>"
            visibleRow=visibleRow + "<td><span class='visibleRowItem'>" + visibleArray[x]["altitude"] + "</span></td>"
            visibleRow=visibleRow + "<td><span class='visibleRowItem'>" + visibleArray[x]["days"] + "</span></td>"
            visibleRow=visibleRow + "<td><span class='visibleRowItem'>" + visibleArray[x]["azimuth"] + "</span></td>"
            visibleRow=visibleRow + "</tr>"
            rv=rv+ visibleRow
        return rv

    def createHtml(self, mmsi, dt, lat, lon, hitData):      
        responseStr=hitData["response"]
        responseJSON=json.loads(responseStr)

        hitmissdata=responseJSON["hitmiss"]
        hitmisssContent=self.createHitMissSummaryContent(hitmissdata)

        visibleData=responseJSON["visible"]
        visibleArray=self.calculateVisibleData(visibleData)
        visibleContent=self.createVisibleSummaryContent(visibleArray)
        
        templateFile="hittesttemplate.html"
        rendered = render_template(templateFile, title='MMSI Hits and Misses', mmsi=mmsi, timestamp=dt, lat=lat, lon=lon, hitMisscContent=Markup(hitmisssContent), visibleContent=Markup(visibleContent))        
        return(rendered)

