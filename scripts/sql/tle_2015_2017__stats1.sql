select satellite, min(ts) as min_ts, avg(1.0*ts), max(ts), (max(ts)-min(ts))/(24*3600), min(dt) as min_dt, max(dt), count(*), sum(valid) as valid
from af_vault.tle_2015_2017
group by satellite
order by valid, min_ts;
