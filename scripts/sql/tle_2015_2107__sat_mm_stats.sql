select valid, satellite, 
    count(*) as n, 
    min(cast(substring(line2, 53, 11) as float)) as min_mm, 
    avg(cast(substring(line2, 53, 11) as float)) as ave_mm, 
    max(cast(substring(line2, 53, 11) as float)) as max_mm, 
    sum(cast(substring(line2, 53, 11) as float)) as sum_mm,
    stddev(cast(substring(line2, 53, 11) as float)) as sdv_mm
from af_vault.tle_2015_2017
group by valid, satellite
order by valid, ave_mm

