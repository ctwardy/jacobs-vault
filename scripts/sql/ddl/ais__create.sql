CREATE DATABASE IF NOT EXISTS af_vault;
DROP TABLE IF EXISTS af_vault.ais;
CREATE EXTERNAL TABLE af_vault.ais(
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
    Cargo INT
)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    LOCATION '/ingest/airforce/vault/ais/'
    TBLPROPERTIES("skip.header.line.count"="1")
;
