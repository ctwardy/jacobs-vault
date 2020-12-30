import gzip
import io
import os
import sys

YEAR_STR=sys.argv[1]
SHIP_STAGE_PATH="/share/nas2/data/airforce/VAULT_Data/demo/ships"

CURRENT_MMSI=""
CURRENT_LINES=[]

def log_it():
    sys.stderr.write(" " + os.path.join(SHIP_STAGE_PATH, YEAR_STR, CURRENT_MMSI + ".tab.gz \\ \n"))
#

def decimate_lines():
    global CURRENT_MMSI
    global CURRENT_LINES
    r = CURRENT_LINES
    n = len(CURRENT_LINES)
    if n>100:
        f = 0.0
        deci_lines = []
        deci_lines.append(CURRENT_LINES[0])
        for i in range(98):
             deci_lines.append(CURRENT_LINES[ ((i+1)*(n-1)) // 98 ])
        if CURRENT_LINES[-1] != deci_lines[-1]:
            deci_lines.append(CURRENT_LINES[-1])
        r = deci_lines
    return r
#

def save_ship(new_mmsi):
    global CURRENT_MMSI
    global CURRENT_LINES
    if len(CURRENT_LINES) > 0:
        filename = mmsi + ".tab.gz"
        filepath = os.path.join(SHIP_STAGE_PATH, YEAR_STR, filename)
        fd = gzip.open(filepath, mode="wt")
        for line in decimate_lines():
            fd.write(line + '\n')
    CURRENT_MMSI = new_mmsi
    CURRENT_LINES = []
#

for line in sys.stdin:
    line = line.rstrip()
    Fields = line.split('\t')
    if len(Fields) > 0:
        mmsi = Fields[0]
        if mmsi != CURRENT_MMSI:
            save_ship(mmsi)
        CURRENT_LINES.append(line)

if len(CURRENT_LINES) > 0:
    save_ship("")

