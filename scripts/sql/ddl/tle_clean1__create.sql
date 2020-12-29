DROP TABLE IF EXISTS af_vault.tle_clean1;
CREATE TABLE af_vault.tle_clean1
AS
SELECT ts, satellite, dt, concat(substring(line1, 1, 64), substring(line1, length(line1)-4,4)) as line1, substring(line2,1,69) as line2
FROM af_vault.tle
SORT BY ts

