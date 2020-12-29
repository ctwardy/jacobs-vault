#!/bin/bash
hive -e "select date_add('1999-12-31', day) as dt_day2, satellite, date_add('1999-12-31', day) as day_dt, day, dt as tle_dt, ts as tle_ts, line1, line2 from af_vault.daily_sat_2015_2017 order by dt_day2, satellite;" | python daily_files__create.py
