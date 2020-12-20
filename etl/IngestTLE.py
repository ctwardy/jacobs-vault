from sgp4.api import Satrec
import sys, io, math, time, datetime

def unixtime_from_sat_time(epoch_year, epoch_day):
    d = datetime.date(2000 + epoch_year,1,1)
    ts = int(math.floor(time.mktime(d.timetuple()) + (24*60*60*epoch_day)))
    return ts
#
def get_meta(line1, line2):
    satellite_rec = Satrec.twoline2rv(line1, line2)
     
    ts = unixtime_from_sat_time(satellite_rec.epochyr, satellite_rec.epochdays)
    dt = datetime.datetime.fromtimestamp(ts)
    return str(ts), str(satellite_rec.satnum), dt.strftime('%Y-%m-%d %H:%M:%S')
#

for line in sys.stdin:
    line = line.rstrip()
    if line[0:2] == "1 ":
        line1 = line
    elif line[0:2] == "2 ":
        line2 = line
        ts_str, satnum_str, dt_str = get_meta(line1, line2)
        out_line = '\t'.join([ts_str, satnum_str, dt_str, line1, line2]) + '\n'
        sys.stdout.write(out_line)
#
