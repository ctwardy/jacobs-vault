select 
    count(*) as total_records, 
    sum(case when substring(validity,1,1) = "_"
             then 1
             else 0
             end) as invalid_mmsi_count,
    -- 2 : D DateTime
    -- 3 : l Latitude
    -- 4 : L Longitude
    sum(case when substring(validity,5,1) = "_"
             then 1
             else 0
             end) as invalid_sog_count,
    sum(case when substring(validity,6,1) = "_"
             then 1
             else 0
             end) as invalid_cog_count,
    sum(case when substring(validity,7,1) = "_"
             then 1
             else 0
             end) as invalid_heading_count,
    sum(case when substring(validity,8,1) = "_"
             then 1
             else 0
             end) as invalid_imo_count,
    sum(case when substring(validity,9,1) = "_"
             then 1
             else 0
             end) as invalid_type_count,
    sum(case when substring(validity,10,1) = "_"
             then 1
             else 0
             end) as invalid_status_count
from af_vault.ais_validity
where substring(basedatetime, 1, 4) == "2017"
;
