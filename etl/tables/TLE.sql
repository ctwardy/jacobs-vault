use vault;

drop table TLE_raw;
create table TLE_raw
(
    filename string,
    linenumber string,
    satellite_cat_number string,
    unknown1 string,
    element_set_epoch string,
    unknown2 string,
    unknown3 string,
    unknown4 string,
    unknown5 string,

    linenumber2 string,
    satellite_cat_number2 string,
    orbin_inclination string,
    right_ascention string,
    eccentricity string,
    arg_perigee string,
    mean_anomaly string,
    mean_motion string,
    revolution_numer string

)

row format delimited
fields terminated by " ";


