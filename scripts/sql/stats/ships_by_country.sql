select L.cc2, sum(A.N) as N, count(distinct A.mmsi) as ship_count
from (
        SELECT mmsi, substring(mmsi, 1, 3) as mid, count(*) as N 
        FROM af_vault.ais
        GROUP BY mmsi, substring(mmsi, 1, 3) 
    ) A
    LEFT JOIN (
        select mmsi_mid, substring(cc2, 1, 2) as cc2 from af_vault.mmsi_mid_cc_lu
    ) L
    ON A.mid = L.mmsi_mid
group by L.cc2
order by ship_count;
