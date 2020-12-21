from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# Create the Spark Session
spark = (
                SparkSession
                    .builder
                    .appName("checksum_error_check")
                    .enableHiveSupport()
                    .getOrCreate()
            )

# Using the geo-processed tables, find out how many records had bad checksums
base = spark.sql("select satellite, error='ValueError: incorrect TLE checksum at end of line' as checksumerror from af_vault.tle_geo")

# Find the number of true/false counts for each satellite
# true -> there was a checksum error encountered
# false -> no checksum error was encountered
df = base.groupBy('satellite','checksumerror').count()
df = df.withColumnRenamed('count','counts')
dfg = df.groupBy('satellite').pivot('checksumerror').agg(F.first('counts'))

# The pivot means there could be null values in the true/false columns
# if a particular satellite had 0 true or false results
dfg = dfg.na.fill(0, subset=['true','false'])
dfg = dfg.withColumn('total', F.col('true') + F.col('false'))
dfg = dfg.withColumn('fraction_error_checksum', F.col('true') / F.col('total'))

# Double check that the total rows from the pivot equal the expected total rows, as a sanity check
tst = spark.table('af_vault.tle')
tst = tst.groupBy('satellite').count()
tstmerge = dfg.join(tst, dfg['satellite']==tst['satellite'])
tstmerge = tstmerge.withColumn('total_counts_equal', tstmerge['total']==tstmerge['count'])
tstmerge.groupBy('total_counts_equal').count().show()

# Write out the results of the fraction of checksums with errors for each satellite to table
dfg.write.saveAsTable('af_vault.tle_geo_checksumerror_fractions')