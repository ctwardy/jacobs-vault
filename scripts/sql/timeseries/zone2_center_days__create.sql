CREATE EXTERNAL TABLE af_vault.zone2_center_days(
    dt STRING,
    lat FLOAT,
    lon FLOAT
)    
    ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
    STORED AS TEXTFILE
    LOCATION '/ingest/airforce/vault/zone2_center_days/'
;
