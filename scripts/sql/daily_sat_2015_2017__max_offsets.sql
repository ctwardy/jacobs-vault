select satellite, max( day - datediff(substring(dt, 1, 10), '1999-12-31') ) as offset from af_vault.daily_sat_2015_2017 group by satellite order by offset;
