select satellite, min(datediff(substring(dt, 1, 10), "1999-12-31")), max(datediff(substring(dt, 1, 10), "1999-12-31"))
from af_vault.tle_2015_2017
where valid=1
group by satellite;

