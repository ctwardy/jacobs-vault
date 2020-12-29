select satellite, min(ts), avg(1.0*ts), max(ts), min(dt), max(dt), count(*) 
from af_vault.tle
group by satellite;
