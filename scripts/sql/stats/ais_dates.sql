select substring(basedatetime, 1, 10) as ymd, count(*) as n from af_vault.ais group by substring(basedatetime, 1, 10) order by ymd;
