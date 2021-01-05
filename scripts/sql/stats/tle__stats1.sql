select 
    satellite, 
    floor((max(ts) - min(ts))/(24*3600)) as day_range_count, 
    min(dt) as dt_min, 
    max(dt) as dt_max, 
    count(distinct substring(dt, 1, 10)) as days_present,
    count(*) as record_count,
    count(distinct substring(dt, 1, 10)) / floor(1 + ((max(ts) - min(ts))/(24*3600))) as present_ratio
from af_vault.tle_all
group by satellite
order by dt_min

