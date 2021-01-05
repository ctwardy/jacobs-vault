from sgp4.api import Satrec
from datetime import datetime
import sgp4.io
import sys, io, math, time

def unixtime_from_sat_time(epoch_year, epoch_day):
    d = datetime.date(1999 + epoch_year,12,31)
    ts = int(math.floor(time.mktime(d.timetuple()) + (24*60*60*epoch_day)))
    return ts
#
def tle_time_to_datetime(tle_time):
    yr = 2000 + int(tle_time[0:2])
    julian_day = int(tle_time[2:5])
    
    julian_day_fract = float("0"+tle_time[5:14])    
    hr_fract = 24 * julian_day_fract
    hr = math.floor(hr_fract)
    mi_fract = 60*(hr_fract - hr)
    mi = math.floor(mi_fract)
    ss_fract = 60*(mi_fract - mi)
    ss = math.floor(ss_fract)
    ms_fract = 1000000*(ss_fract - ss)
    ms = math.floor(ms_fract)
    jdate_str = "%4d%03d %02d:%02d:%02d.%06d"%(yr,julian_day,hr,mi,ss,ms)
    datestd = datetime.strptime(jdate_str, "%Y%j %H:%M:%S.%f")
    return datestd
#
def check_valid(line1, line2):
    is_valid = 0
    try:
        if (sgp4.io.compute_checksum(line1) == int(line1[68:69])) and (sgp4.io.compute_checksum(line2) == int(line2[68:69])):
            is_valid = 1
    except:
        pass
    return is_valid
#
def get_meta(line1, line2):
    satellite_rec = Satrec.twoline2rv(line1, line2)
    dt = tle_time_to_datetime(line1[18:32])
    ts = dt.timestamp()
    is_valid = check_valid(line1, line2)
    
    return str(ts), str(satellite_rec.satnum), dt.strftime('%Y-%m-%d %H:%M:%S'), str(is_valid)
#

line1 = ""
for line in sys.stdin:
    line = line.rstrip()
    line = line[0:69]
    if line[0:2] == "1 ":
        line1 = line
    elif line[0:2] == "2 ":
        line2 = line
        try:
            ts_str, satnum_str, dt_str, is_valid = get_meta(line1, line2)
        except:
            ts_str, satnum_str, dt_str, is_valid = "", "", "", "0"
       
        out_line = '\t'.join([ts_str, satnum_str, dt_str, is_valid, line1, line2]) + '\n'
        sys.stdout.write(out_line)
#
