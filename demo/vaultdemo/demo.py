from branca.colormap import linear
from datetime import datetime
from dateutil import tz
from ipyleaflet import (AntPath, Map, Circle, GeoData, basemaps, WidgetControl, GeoJSON,
 LayersControl, LayerGroup, Icon, Marker,basemap_to_tiles, Choropleth,
 MarkerCluster, Heatmap,SearchControl,
 FullScreenControl)
from ipywidgets import Text, HTML
from shapely.geometry import Point
import fiona
import geopandas as gpd
import json
import math
import os
import pandas as pd
import plotly.express as px

from vault.hittest import HitTest, DAY_FILE_PATH

AIS_COLUMNS=["mmsi", "basedatetime", "lat", "lon", "sog", "cog", "heading", "vesselname", "imo", "callsign", "vesseltype", "status, length", "width", "draft", "cargo"]
AIS_TYPES=[   str,    str,           float, float, object, object, object,     str,           str, object,         object,           str,    object,   object,    object,   object]

# Adapted from:
#   https://gist.github.com/amites/3718961
def center_geolocation(lats, lons):
    """
    Provide a relatively accurate center lat, lon returned as a list pair, given
    a list of list pairs.
    ex: in: iterative latitude and longitude list-likes in degrees
        out: (center_lat, center_lon)
    """
    d2r = 180.0/math.pi
    
    x = 0.0
    y = 0.0
    z = 0.0
    n = 0

    for lat, lon in zip(lats, lons):
        lat = lat / d2r
        lon = lon / d2r
        x += math.cos(lat) * math.cos(lon)
        y += math.cos(lat) * math.sin(lon)
        z += math.sin(lat)
        n += 1

    x_avg = x / n
    y_avg = y / n
    z_avg = z / n
    
    lat_out = math.atan2(z_avg, math.sqrt((x_avg**2 ) + (y_avg**2))) * d2r
    lon_out = math.atan2(y_avg, x_avg) * d2r
    
    return (lat_out, lon_out)
#

HTML_TEMPLATE='''
<h3>%s</h3>
<h4>%3.4f, %3.4f<h4>
<h4>%s<h4>
'''

class Demo:

    def __init__(self, year, mmsi, ship_data_root="../data/VAULT_Data/demo/ships"):
        year = str(year)
        mmsi = str(mmsi)

        ship_path = os.path.join(ship_data_root, year, mmsi+".tab.gz")
        # "index_col=False" important here to keep column alignment as expected
        self.df_ais = pd.read_csv(ship_path, sep='\t', compression='gzip', names=AIS_COLUMNS, dtype=dict(zip(AIS_COLUMNS, AIS_TYPES)), index_col=False)
        self.geom_ais = [Point(xy) for xy in zip(self.df_ais.lat, self.df_ais.lon)]
        self.ais_gdf = gpd.GeoDataFrame(self.df_ais, geometry=self.geom_ais)

        self.ais_geodata = GeoData(geo_dataframe=self.ais_gdf, name="AIS")
        self.center = center_geolocation(self.df_ais["lat"], self.df_ais["lon"])
    #
    def setShipPathLayerGroup(self):
        layer_group = LayerGroup()
        def circleForRow(row):
            circle = Circle(location=(row["lat"], row["lon"]), radius=100, color="orange", fill_color="yellow")
            circle.popup = HTML('{"dt": "%s", "lat": %3.4f, "lon": %3.4f}'%(row["basedatetime"], row["lat"], row["lon"]))
            layer_group.add_layer(circle)
        #
        self.df_ais.apply(circleForRow, axis=1)
        self.map.add_layer(layer_group)
    #
    def show_map(self):
        zoom = 9
        self.map = Map(basemap=basemaps.Esri.WorldImagery, center=self.center, zoom=zoom)
        ant_path = AntPath(
            locations=list(zip(self.df_ais["lat"], self.df_ais["lon"])),
            dash_array=[1, 10],
            delay=1000,
            color='#7590ba',
            pulse_color='#3f6fba'
        )
        self.map.add_layer(ant_path)
        self.setShipPathLayerGroup()

        vals = self.df_ais.iloc[-1]
        html = HTML_TEMPLATE%(vals["mmsi"], vals["lat"], vals["lon"], vals["basedatetime"])
        html_widget = HTML(html)
        html_widget.layout.margin = '0px 20px 20px 20px'
        html_control = WidgetControl(widget=html_widget, position='topright')
        self.map.add_control(html_control)

        return map
    #
    def hittest(self, dt_lat_lat_hittest_obj):
        dt = datetime.strptime(dt_lat_lat_hittest_obj["dt"], "%Y-%m-%dT%H:%M:%S")
        ht = HitTest(dt)
        
        hit_miss_table, self.df_alt_az_days_visible = ht.invoke(dt, dt_lat_lat_hittest_obj["lat"], dt_lat_lat_hittest_obj["lon"])
        return hit_miss_table
    #
    def starmap(self):
        self.df_alt_az_days_visible["color"] = 2
        self.df_alt_az_days_visible.loc[(self.df_alt_az_days_visible["days"] <= 14.0), "color"] = 1
        self.df_alt_az_days_visible.loc[(self.df_alt_az_days_visible["days"] <= 2.0), "color"] = 0
        self.df_alt_az_days_visible["R"] = 90.0 - self.df_alt_az_days_visible["altitude"]
        fig = px.scatter_polar(self.df_alt_az_days_visible, r="R", theta="azimuth", color="color")
        fig.show()
        

