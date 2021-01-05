select count(*), count(distinct mmsi), min(LAT), max(LAT), min(LON), max(LON), min(SOG), max(SOG), min(COG), max(COG), min(Heading), max(Heading) 
from (
    SELECT mmsi, lat, lon, sog, cog, Heading from af_vault.ais
    UNION ALL
    SELECT mmsi, cast(lat as float), cast(lon as float), cast(sog as float), cast(cog as float), cast(Heading as float) from af_vault.ais_gdb
) T;
