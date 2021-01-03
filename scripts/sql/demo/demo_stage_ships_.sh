#!/bin/bash
#   demo_stage_ships.sh per-year child process
hive -e "select * from af_vault.ais where substring(basedatetime,1,4)='"$1"' order by mmsi, basedatetime;" | \
    python demo_stage_ships.py $1
