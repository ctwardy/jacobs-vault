from branca.colormap import linear
from datetime import datetime
from dateutil import tz
from ipyleaflet import (Map, GeoData, basemaps, WidgetControl, GeoJSON,
 LayersControl, Icon, Marker,basemap_to_tiles, Choropleth,
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

class Demo:

    def __init__(self, year, mmsi):
        year = str(year)
        mmsi = str(mmsi)

        ship_path = os.path.join("/share/nas2/data/airforce/VAULT_Data/demo/ships", year, mmsi+".tab.gz")
        # "index_col=False" important here to keep column alignment as expected
        df_ais = pd.read_csv(ship_path, sep='\t', compression='gzip', names=AIS_COLUMNS, dtype=dict(zip(AIS_COLUMNS, AIS_TYPES)), index_col=False)
        df_ais2 = df_ais[["mmsi", "lat", "lon", "basedatetime"]]
        geom_ais = [Point(xy) for xy in zip(df_ais2.lat, df_ais2.lon)]
        ais_gdf = gpd.GeoDataFrame(df_ais2, geometry=geom_ais)

        this.ais_geodata = GeoData(geo_dataframe=ais_gdf, name="AIS")
        this.center = center_geolocation(df_ais["lat"], df_ais["lon"])
    #
    def show_map(self):
        zoom = 5
        this.map = Map(basemap=basemaps.Esri.WorldImagery, center=this.center, zoom=zoom)
        this.map.add_layer(this.ais_geodata)
        this.map.show()
    #
    def hittest(self, dt_lat_lat_hittest_str):
        print("testing hit")

