hive -e 'select satellite, datediff(substring(dt, 1, 10), "1999-12-31") as day, ts, dt, line1, line2 from af_vault.tle_2015_2017 where satellite in ("10234", "10252", "10289") order by satellite, day;' > daily_sat_sample_input.tab
python daily_sat.py < daily_sat_sample_input.tab
