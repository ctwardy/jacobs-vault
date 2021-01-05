select 
    substring(dt, 1, 4) as year,
    valid,
    count(distinct satellite) as satellite_count,
    count(distinct substring(dt, 1, 10)) as days_present,
    count(*) as record_count
from af_vault.tle_all
group by substring(dt, 1, 4), valid
order by year, valid

