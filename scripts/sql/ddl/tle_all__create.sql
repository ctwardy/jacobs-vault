-- Create the tle_all table from our seperate ingests
-- ... and fix the datetime year issue

DROP TABLE IF EXISTS af_vault.tle_all;

CREATE TABLE af_vault.tle_all
--PARTITIONED BY (year)
STORED AS PARQUET
AS
SELECT unix_timestamp(dt) as ts, satellite, dt, valid, line1, line2, year
FROM (
    select satellite, 
        case when cast(substring(dt, 3, 2) as int) > 50
             then concat("19", substring(dt, 3))
             else concat("20", substring(dt, 3))
             end as dt,
        valid, line1, line2,
        case when cast(substring(dt, 3, 2) as int) > 50
             then cast(concat("19", substring(dt, 3, 2)) as int)
             else cast(concat("20", substring(dt, 3, 2)) as int)
             end as year
        from af_vault.tle_2015_2017
    union all
    select satellite, 
        case when cast(substring(dt, 3, 2) as int) > 50
             then concat("19", substring(dt, 3))
             else concat("20", substring(dt, 3))
             end as dt,
        valid, line1, line2,
        case when cast(substring(dt, 3, 2) as int) > 50
             then cast(concat("19", substring(dt, 3, 2)) as int)
             else cast(concat("20", substring(dt, 3, 2)) as int)
             end as year
        from af_vault.tle_other
) T;

