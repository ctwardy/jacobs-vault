ADD FILE daily_sat.py;
ADD FILE tle_sat_day_minmax.tab;

DROP TABLE IF EXISTS af_vault.daily_sat_2015_2017;
CREATE TABLE af_vault.daily_sat_2015_2017
AS
SELECT TRANSFORM(T.satellite, T.day, T.ts, T.dt, T.line1, T.line2)
    USING '/opt/anaconda/bin/python daily_sat.py' 
    AS (satellite STRING, day INT, ts INT, dt STRING, line1 STRING, line2 STRING)
FROM (
    select satellite, datediff(substring(dt, 1, 10), "1999-12-31") as day, ts, dt, line1, line2
    from af_vault.tle_2015_2017
    where valid=1
    DISTRIBUTE BY satellite
    SORT BY satellite, ts
) T;


