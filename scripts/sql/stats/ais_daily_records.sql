SELECT ymd, n
FROM (
    select substring(basedatetime, 1, 10) as ymd, count(*) as n from af_vault.ais group by substring(basedatetime, 1, 10)
    union all
    select substring(basedatetime, 1, 10) as ymd, count(*) as n from af_vault.ais_gdb group by substring(basedatetime, 1, 10)
) T
order by ymd;

