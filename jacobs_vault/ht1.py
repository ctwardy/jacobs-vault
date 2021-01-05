# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_Early_HitTest.ipynb (unless otherwise specified).

__all__ = ['COLUMNS', 'DTYPES', 'DATE_COLS', 'load_day_file', 'DAY_FILE_PATH', 'test_skyfield', 'satellite_alt_az_days',
           'hit_quality', 'viz']

# Cell
# Supposed to be "hide" but that keeps the module from having imports.

# Mostly test nbdev is set up right
# If you get ModuleNotFound, either symlink nbs/jacobs_vault -> jacobs_vault, or
# in each notebook `import sys; sys.path.append('..')`.
from .template import *

from datetime import datetime
from dateutil import tz
from skyfield.api import EarthSatellite
from skyfield.api import Topos, load
import math
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

# Cell
COLUMNS = ["satellite", "day_dt", "day", "tle_dt", "tle_ts", "line1", "line2"]
# DTYPES = [str, str, int, str, int, str, str]
DTYPES = {'satellite': 'uint16', # observed values are ints in 5..41678, so 0..65535 is good
          'day_dt': 'str',       # here a single date, but generally datetime: PARSE
          'day': 'uint16',       # here a single value 6026, too big for uint8, but 16 is good
          'tle_dt': 'str',       # again, PARSE AS DATETIME
          'tle_ts': 'uint32',    # large ints, but < 4294967295. We could compress more, but... meh
          'line1': 'string',     # 12K unique 80-char TLE strings. Category wd give tiny compression.
          'line2': 'string'}     # In theory "string" is better than "object". Not seeing it here.

DATE_COLS = ['day_dt', 'tle_dt']

# Cell
DAY_FILE_PATH="data/VAULT_Data/TLE_daily"  # Assumes symlink nbs/data -> actual data folder.

def load_day_file(_day:datetime, folder:str=DAY_FILE_PATH, date_cols=DATE_COLS, verbose=True):
    """Look for and load TLE datafile for {_day}."""
    df_path = "%s/%4d/%02d/%02d.tab.gz"%(folder, _day.year, _day.month, _day.day)
    if verbose:
        print(f'{_day}\t{df_path}')
    df = pd.read_csv(df_path,
                     names=COLUMNS, sep='\t', compression='gzip',
                     dtype=DTYPES,
                     parse_dates=date_cols,
                     infer_datetime_format=True)
    return df

# Cell
def test_skyfield():
    lat =  45.0
    lon = -176.0
    earth_position = Topos(lat, lon)

    ts = load.timescale()
    t = ts.utc(datetime(2016, 6, 30).replace(tzinfo=tz.tzutc()))

    line1="1 10000U 77034A   16182.45131225 -.00000171  00000-0  00000+0 0  1275"
    line2="2 10000  15.5820 331.7785 0019081 259.0540  28.2803  0.96674507130362"
    satellite = EarthSatellite(line1, line2, '77034', ts)

    difference = satellite - earth_position

    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()

    print(f'{alt.degrees:.1f}º, {az.degrees:.1f}º, {distance.km:.1f}km')
#
test_skyfield()

# Cell
def satellite_alt_az_days(_t0: datetime, lat: float, lon: float):
    '''Load tracks for day {_t0} and return altitiude, azimuth, and 𝚫t [days] for each row.

    '''
    earth_position = Topos(lat, lon)

    ts = load.timescale()
    t = ts.utc(_t0.replace(tzinfo=tz.tzutc()))

    def eval_tle(row):
        '''Extract satellite info from line1/line2/tle_dt.

        Returns alt, az, and (days between dt and each row).
        Inherits {ts}, {t}, and {earth_position} values at function definition.

        TODO: Currently only works for `apply(raw=False)`.

        '''
        try:
            satellite = EarthSatellite(row['line1'], row['line2'], 'x', ts)
            𝚫t = abs(_t0 - row['tle_dt'])
        except IndexError:
            # `apply(raw=True)` sends arrays instead of Series
            satellite = EarthSatellite(row[5], row[6], 'x', ts)
            𝚫t = abs(_t0 - row[3])
        topocentric = (satellite - earth_position).at(t)
        alt, az, distance = topocentric.altaz()
        return pd.Series([alt.degrees, az.degrees, 𝚫t])

    df = load_day_file(_t0).drop_duplicates()
    df_alt_az_days = pd.DataFrame(df.apply(eval_tle, axis=1, raw=False))
    df_alt_az_days.columns = ["altitude", "azimuth", "days"]
    #df_alt_az_days.reindex()
    return df_alt_az_days

# Cell
def hit_quality(df_alt_az_days):
    """Return hit/miss and quality as time proximity.

    Parameters
    ----------
    `df_alt_az_days`: Dataframe returned by `satellite_alt_az_days`.

    Returns
    --------
    Dataframe with columns ["hit", "miss"]. Each row will have exactly one filled, with
    a string denoting how recent the pass was, e.g. "excellent", "good", "poor", "stale".

    """

    def eval_quality(row):
        """Inner function to be `apply`d to a dataframe."""
        ser = None
        days = row[2].days
        altitude = row[0]
        if days <= 2.0:
            if altitude > 0.0:
                vals = ["excellent", math.nan]
            else:
                vals = [math.nan, "excellent"]
        elif days <= 14.0:
            if altitude > 0.0:
                vals = ["good", math.nan]
            else:
                vals = [math.nan, "good"]
        elif days <= 56.0:
            if altitude > 0.0:
                vals = ["poor", math.nan]
            else:
                vals = [math.nan, "poor"]
        else:
            vals = [math.nan, "stale"]

        return pd.Series(vals)

    df_hit_quality = pd.DataFrame(df_alt_az_days.apply(eval_quality, axis=1))
    df_hit_quality.columns = ["hit", "miss"]
    return df_hit_quality
#

# Cell
def viz(df, show=True, size0=1):
    """Polar plots a `df_alt_az_days_visible` dataframe.
    Dataframe must have: `color`, `days`, `altitude`, `azimuth`.
    Returns a Plotly Express polar plot figure.
    If show=True, also displays it here.
    size0 is the smallest marker size (used for best hits)

    """
    df["color"] = 2
    df.loc[(df["days"].dt.days <= 14.0), "color"] = 1
    df.loc[(df["days"].dt.days <= 2.0), "color"] = 0
    df["size"] = size0 + df["color"]*2
    df["R"] = 90.0 - df["altitude"]
    #fig = px.scatter_polar(df_alt_az_days_visible, r="R", theta="azimuth", color_discrete_sequence=['black'])
    fig = px.scatter_polar(df_alt_az_days_visible, r="R", theta="azimuth",
                           color="color", size="size", size_max=10, render_mode='webgl')
    if show:
        fig.update_traces(opacity=.5).show()
    return fig