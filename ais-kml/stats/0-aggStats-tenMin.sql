set mapreduce.map.memory.mb=8192;
set mapreduce.reduce.memory.mb=8192;
set mapreduce.map.java.opts=-Xmx8g;
set mapreduce.reduce.java.opts=-Xmx8g;
set mapred.compress.map.output=true;
set mapred.output.compres=true;
set hive.vectorized.execution.enabled=true;
set parquet.compression=SNAPPY;
set mapred.output.compression.codec=org.apache.hadoop.io.compress.SnappyCodec;
set mapred.output.compression.type=BLOCK;
set hive.exec.compress.output=true;

use af_vault;

create table ais_agg_stats_tenmin stored as parquet as 
select 
	mmsi, 
	substr(basedatetime,0,4)  as year, 
	CONCAT(substr(basedatetime,0,15),"0:00") as datetime,

	min(cast(sog as float)) as sog_min,
        max(cast(sog as float)) as sog_max,
        avg(cast(sog as float)) as sog_avg,

        min(cast(cog as float)) as cog_min,
        max(cast(cog as float)) as cog_max,
        avg(cast(cog as float)) as cog_avg,

        avg(cast(heading as float)) as heading_avg,

        vesselname,
        imo,
        callsign,
        vesseltype,
        status,
        length,
        width,

        min(cast(draft as float)) as draft_min,
        max(cast(draft as float)) as draft_max,
        avg(cast(draft as float)) as draft_avg,

        cargo,

        min(cast(lat as float)) as lat_min,
        max(cast(lat as float)) as lat_max,
        avg(cast(lat as float)) as lat_avg,

        min(cast(lon as float)) as lon_min,
        max(cast(lon as float)) as lon_max,
        avg(cast(lon as float)) as lon_avg,


        count(1) as cnt

from
        ais

group by
        mmsi,
        substr(basedatetime,0,4),
        substr(basedatetime,0,15),
        vesselname,
        imo,
        callsign,
        vesseltype,
        status,
        length,
        width,
        cargo;


