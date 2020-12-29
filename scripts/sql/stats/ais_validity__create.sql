ADD FILE validity_scan.py;
ADD FILE MMSI_MID_CC_LU.tab;

DROP TABLE IF EXISTS af_vault.ais_validity;
CREATE TABLE af_vault.ais_validity
AS 
SELECT TRANSFORM(mmsi, basedatetime, lat, lon, sog, cog, heading, vesselname, imo, callsign, vesseltype, status, length, width, draft, cargo)
    USING '/opt/anaconda/bin/python validity_scan.py'
    AS (
        `mmsi` string, 
        `basedatetime` string, 
        `lat` float, 
        `lon` float, 
        `sog` float, 
        `cog` float, 
        `heading` float, 
        `vesselname` string, 
        `imo` string, 
        `callsign` string, 
        `vesseltype` string, 
        `status` string, 
        `length` float, 
        `width` float, 
        `draft` float, 
        `cargo` int,
        `validity` string
    )
FROM (
    select mmsi, basedatetime, lat, lon, sog, cog, heading, vesselname, imo, callsign, vesseltype, status, length, width, draft, cargo 
    from af_vault.ais
    distribute by mmsi
) T;

