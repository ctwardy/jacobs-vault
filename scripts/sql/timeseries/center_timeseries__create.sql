ADD FILE center_timeseries.py;
ADD FILE hittestservice_deps.zip;

-- Force one mapper per day
SET mapreduce.input.fileinputformat.split.maxsize=768;

DROP TABLE IF EXISTS af_vault.center_timeseries;
CREATE TABLE af_vault.center_timeseries
AS
SELECT TRANSFORM(dt, lat, lon)
    USING '/opt/anaconda/bin/python center_timeseries.py'
    AS (dt STRING, lat FLOAT, lon FLOAT, hit_excellent int, hit_good int, hit_poor int, miss_excellent int, miss_good int, miss_poor int, expired int, dataframe STRING)
    FROM af_vault.zone2_center_days
;
