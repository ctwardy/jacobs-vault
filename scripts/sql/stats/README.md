# SQL scripts for overview stats

These scripts were run using hive with command lines that look like:
<pre>
hive -f <i>sql-file-base-name.sql</i>  <b> > </b>  ../../../data/VAULT_Data/stats_out/<i>sql-file-base-name.tab</i>
</pre>

These scripts are predicated on the existence of the af_vault 
database created as part of the ETL process

