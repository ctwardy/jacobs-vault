SELECT T.utc_day, SUM(T.orbits_per_day) as orbits_per_day
FROM (
    select satellite, substring(dt, 1, 10) as utc_day,
        avg(cast(substring(line2, 53, 10) as float)) as orbits_per_day
    from af_vault.tle
    group by satellite, substring(dt, 1, 10)
) T
GROUP BY T.utc_day
ORDER BY T.utc_day;

