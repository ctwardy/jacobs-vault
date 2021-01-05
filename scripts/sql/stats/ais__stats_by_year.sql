select
  substring(BaseDateTime, 1, 4) as year,
  count(distinct MMSI) as ship_count,
  count(*) as record_count
from (
    SELECT BaseDateTime, MMSI FROM af_vault.ais
    UNION ALL
    SELECT basedatetime, mmsi FROM af_vault.ais_gdb
) T
group by substring(BaseDateTime, 1, 4)
order by year

