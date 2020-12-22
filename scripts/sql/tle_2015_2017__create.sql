DROP TABLE IF EXISTS af_vault.tle_2015_2017;
CREATE EXTERNAL TABLE af_vault.tle_2015_2017(
    ts INT,
    satellite STRING,
    dt STRING,
    valid int,
    line1 STRING,
    line2 STRING
)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
    STORED AS TEXTFILE
    LOCATION '/ingest/airforce/vault/tle_2015_2017_2/'
;
