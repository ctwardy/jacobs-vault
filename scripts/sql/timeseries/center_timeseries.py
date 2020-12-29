import sys, io
import json
sys.path.append("hittestservice_deps.zip")
from vault.hittest import HitTest
from datetime import datetime
import pandas as pd
import time

CURRENT_DATE = ""

ht = None

for line in sys.stdin:
    line = line.rstrip()
    A = line.split('\t')
    if len(A) >= 3:
        dt_str, lat_str, lon_str = A[0:3]
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        date_str = dt_str[0:10]
        if date_str != CURRENT_DATE:
            ht = HitTest(dt, "/share/nas2/data/vault/TLE_daily")
            CURRENT_DATE = date_str
        json_str = ht.invoke(dt, float(lat_str), float(lon_str))
        D = json.loads(json_str)
        R = [
            str(D["hitmiss"]["0"]["Excellent"]),
            str(D["hitmiss"]["0"]["Good"]),
            str(D["hitmiss"]["0"]["Poor"]),
            str(D["hitmiss"]["1"]["Excellent"]),
            str(D["hitmiss"]["1"]["Good"]),
            str(D["hitmiss"]["1"]["Poor"]),
            str(D["hitmiss"]["1"]["Stale"]),
            str(D["visible"])
        ]
        out_line = '\t'.join(A+R)
        sys.stdout.write(out_line + '\n')

sys.stdout.flush()
time.sleep(1)
