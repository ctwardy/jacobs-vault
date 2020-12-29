DROP TABLE IF EXISTS af_vault.tle_other;
CREATE EXTERNAL TABLE af_vault.tle_other(
    ts INT,
    satellite STRING,
    dt STRING,
    valid int,
    line1 STRING,
    line2 STRING
)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
    STORED AS TEXTFILE
    LOCATION '/ingest/airforce/vault/tle_other/'
;
