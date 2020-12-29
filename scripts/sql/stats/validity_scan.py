import sys, io 
from datetime import datetime
import time

def load_mmsi_mid_lu():
    S = set([])
    with open("MMSI_MID_CC_LU.tab") as f:
        for line in f:
            line = line.rstrip()
            A = line.split('\t')
            if len(A) > 0:
                mmsi_mid = A[0]
                S.add(mmsi_mid)
    return S
#
VALID_MMSI_MID_SET = load_mmsi_mid_lu()

# AIS valid field range documentation:
#   https://www.navcen.uscg.gov/?pageName=AISFAQ


def v_mmsi(mmsi):
    valid = True
    if len(mmsi) != 9:
        valid = False
    elif mmsi[0:3] not in VALID_MMSI_MID_SET:
        valid = False
    return valid
#
def v_dt(dt):
    valid = True
    try:
        _ = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    except:
        valid = False
    return valid
#
def v_lat(lat):
    valid = True
    try:
        x = float(lat)
        if not ((-90.0 <= x) and (x <= 90.0)):
            valid = False
    except:
        valid = False
    return valid
#
def v_lon(lon):
    valid = True
    try:
        x = float(lon)
        if not ((-180.0 <= x) and (x <= 180.0)):
            valid = False
    except:
        valid = False
    return valid
#
def v_sog(sog):
    valid = True
    try:
        x = float(sog)
        if not ((0.0 <= x) and (x <= 102.4)):
            valid = False
    except:
        valid = False
    return valid
#
def v_cog(cog):
    valid = True
    try:
        x = float(cog)
        if not ((0.0 <= x) and (x <= 102.4)):
            valid = False
    except:
        valid = False
    return valid
#
def v_heading(heading):
    valid = True
    try:
        x = int(heading)
        if not ( heading == 511 or ( 0 <= heading and heading < 360 )):
            valid = False
    except:
        valid = False
    return valid
#
def v_vesselname(vesselname):
    return True
#
def v_imo(imo):
    valid = True
    try:
        if len(imo) != 0:
            if imo[0:3] != "IMO":
                valid = False
            if len(imo) != 10:
                valid = False
    except:
        valid = False
    return valid
#
def v_callsign(callsign):
    return True
#
VALID_VESSEL_TYPES = [0] + list(range(20,25,1)) + list(range(30,38,1)) + list(range(40,45,1)) + \
    list(range(49,65,1)) + list(range(69,75,1)) + list(range(79,85,1)) + list(range(89,95,1)) + [99]

def v_vesseltype(vesseltype):
    valid = True
    try:
        vesseltype = int(vesseltype)
        if vesseltype not in VALID_VESSEL_TYPES:
            valid = False
    except:
        valid = False
    return valid
#
VALID_STATUS_STR = [
    "under way using engine",
    "at anchor",
    "not under command",
    "restricted maneuverability",
    "constrained by her draught",
    "moored",
    "aground",
    "engaged in fishing",
    "under way sailing",
    "AIS-SART (active); MOB-AIS; EPIRB-AIS",
    "undefined"
]
def v_status(status):
    if status in VALID_STATUS_STR:
        return True
    else:
        return False
#
# Ignoring length, width, draft and cargo.
#  If width were just coming from an AIS message it would be limited to integers 0..126 , we have floats
#  If length were just coming from an AIS message it would be limited to integers 0..1022, we have floats
#  If draft were just coming from an AIS message, it would be limited to decimals 0..25.5  (0..255 in 1/10 meters) 
#

for line in sys.stdin:
    line = line.rstrip()
    Fields = line.split('\t')
    valid_tag = ""
    if len(Fields) == 16:
        (mmsi, dt, lat, lon, sog, cog, heading, vesselname, imo, callsign, vesseltype, status, length, width, draft, cargo) = Fields
        valid_tag = ["M","D","l","L","S","C","H","I","T","S"]
        idx = 0
        if not v_mmsi(mmsi):
            valid_tag[idx] = "_"
        idx = idx + 1
        if not v_dt(dt):
            valid_tag[idx] = "_"
        idx = idx + 1
        if not v_lat(lat):
            valid_tag[idx] = "_"
        idx = idx + 1
        if not v_lon(lon):
            valid_tag[idx] = "_"
        idx = idx + 1
        if not v_sog(sog):
            valid_tag[idx] = "_"
        idx = idx + 1
        if not v_cog(cog):
            valid_tag[idx] = "_"
        idx = idx + 1
        if not v_heading(heading):
            valid_tag[idx] = "_"
        idx = idx + 1
        if not v_imo(imo):
            valid_tag[idx] = "_"
        idx = idx + 1
        if not v_vesseltype(vesseltype):
            valid_tag[idx] = "_"
        idx = idx + 1
        if not v_status(status):
            valid_tag[idx] = "_"

        valid_tag = "".join(valid_tag)
    #
    sys.stdout.write(line + '\t' + valid_tag + '\n')
#
sys.stdout.flush()
time.sleep(1)
