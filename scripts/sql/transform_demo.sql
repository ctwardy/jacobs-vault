ADD FILE transform_demo.py;

select transform (T.satellite, T.line1, T.line2 ) 
    using '/opt/anaconda/bin/python transform_demo.py' 
    as (satellite STRING, n INT)
from (
    SELECT satellite, line1, line2 
    FROM af_vault.tle
    DISTRIBUTE BY satellite
) T;
