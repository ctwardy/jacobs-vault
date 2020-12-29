select status, count(*) as n from af_vault.ais group by status order by status;
