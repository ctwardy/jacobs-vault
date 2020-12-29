select mmsi, imo, vesselname, callsign, vesseltype, length, width, 
    count(*), min(basedatetime), max(basedatetime), avg(sog), min(sog), max(sog) 
from af_vault.ais 
group by mmsi, imo, vesselname, callsign, vesseltype, length, width;
