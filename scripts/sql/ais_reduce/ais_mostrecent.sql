create table af_vault.ais_mostrecent
as
select mmsi, basedatetime, lat, lon, sog, cog, heading, vesselname, imo, callsign, vesseltype, status, length, width, draft, cargo
from (
    SELECT 
        ROW_NUMBER() OVER(PARTITION BY mmsi ORDER BY basedatetime DESC) as rn,
        mmsi, basedatetime, lat, lon, sog, cog, heading, vesselname, imo, callsign, vesseltype, status, length, width, draft, cargo
    FROM af_vault.ais
) T
where T.rn=1
