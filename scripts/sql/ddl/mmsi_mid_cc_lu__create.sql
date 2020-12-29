DROP TABLE IF EXISTS af_vault.mmsi_mid_cc_lu;
CREATE EXTERNAL TABLE af_vault.mmsi_mid_cc_lu(
    mmsi_mid STRING,
    country STRING,
    cc2 STRING,
    cc3 STRING
)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
    STORED AS TEXTFILE
    LOCATION '/ingest/airforce/vault/mmsi_mid_cc_lu'
;

