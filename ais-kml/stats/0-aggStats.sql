
use vault;

create table ais_agg_stats_dmac stored as parquet as 
select 
	mmsi, 
	substr(basedatetime,0,4)  as year, 
	substr(basedatetime,0,10) as datetime,

	min(cast(sog as decimal)) as sog_min,
        max(cast(sog as decimal)) as sog_max,
        avg(cast(sog as decimal)) as sog_avg,

        min(cast(cog as decimal)) as cog_min,
        max(cast(cog as decimal)) as cog_max,
        avg(cast(cog as decimal)) as cog_avg,

        avg(cast(heading as decimal)) as heading_avg,

        vesselname,
        imo,
        callsign,
        vesseltype,
        status,
        length,
        width,

        min(cast(draft as decimal)) as draft_min,
        max(cast(draft as decimal)) as draft_max,
        avg(cast(draft as decimal)) as draft_avg,

        cargo,

        min(cast(lat as decimal)) as lat_min,
        max(cast(lat as decimal)) as lat_max,
        avg(cast(lat as decimal)) as lat_avg,

        min(cast(lon as decimal)) as lon_min,
        max(cast(lon as decimal)) as lon_max,
        avg(cast(lon as decimal)) as lon_avg,


        count(1) as cnt

from
        ais

group by
        mmsi,
        substr(basedatetime,0,4),
        substr(basedatetime,0,10),
        vesselname,
        imo,
        callsign,
        vesseltype,
        status,
        length,
        width,
        cargo;




