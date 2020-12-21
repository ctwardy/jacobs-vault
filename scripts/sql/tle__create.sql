DROP TABLE IF EXISTS af_vault.tle;
CREATE EXTERNAL TABLE af_vault.tle(
    ts INT,
    satellite STRING,
    dt STRING,
    line1 STRING,
    line2 STRING
)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
    STORED AS TEXTFILE
    LOCATION '/ingest/airforce/vault/tle/'
;
