select satellite, min(ts), avg(1.0*ts), max(ts), (max(ts)-min(ts))/(24*3600), min(dt), max(dt), count(*), sum(valid)
from af_vault.tle_2015_2017
group by satellite;
