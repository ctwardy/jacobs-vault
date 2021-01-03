SELECT ymd, n
FROM (
    select substring(dt, 1, 10) as ymd, count(*) as n from af_vault.tle_other group by substring(dt, 1, 10)
    union all
    select substring(dt, 1, 10) as ymd, count(*) as n from af_vault.tle_2015_2017 group by substring(dt, 1, 10)
) T
order by ymd;

