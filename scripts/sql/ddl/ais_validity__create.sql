DROP TABLE IF EXISTS af_vault.ais_validity;
CREATE EXTERNAL TABLE af_vault.ais_validity(
    MMSI STRING,
    BaseDateTime STRING,
    LAT FLOAT,
    LON FLOAT,
    SOG FLOAT,
    COG FLOAT,
    Heading FLOAT,
    VesselName STRING,
    IMO STRING,
    CallSign STRING,
    VesselType STRING,
    Status STRING,
    Length FLOAT,
    Width FLOAT,
    Draft FLOAT,
    Cargo INT,
    validity STRING
)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
    STORED AS TEXTFILE
    LOCATION '/ingest/airforce/vault/ais_validity/'
;
