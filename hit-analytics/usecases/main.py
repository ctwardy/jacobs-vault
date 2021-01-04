from hitdetector import HitDetector
from hitdetector.utilities import cli_arguments

from pyspark.sql import SparkSession


def main():
    # Initiate a Spark session
    spark = (
                SparkSession
                    .builder
                    .appName("hit-analytics")
                    .enableHiveSupport()
                    .getOrCreate()
            )

    args = cli_arguments()

    spark.conf.set("spark.sql.session.timeZone", "GMT")
    
    # ais = spark.table('cmorris.ais_subset_1000_1100')
    # tle = spark.table('cmorris.tle_2015_2017_subset_1000_1100')

    ais = spark.table('cmorris.af_vault_ais_daily_volume')#.limit(100_000)
    tle = spark.table('af_vault.tle_2015_2017')#_subset_1000_1500')#.limit(1_000_000)

    ais.cache()
    tle.cache()

    # ais = ais.filter(ais['imo']!='')
    tle = tle.filter(tle['satellite']!='')
    tle = tle.filter(tle['valid']==1)

    print("AIS length:", ais.count())
    print("TLE after-filter length:", tle.count())
    # print("Distinct IMO",ais.select('imo').distinct().count())
    print("Distinct satellite",tle.select('satellite').distinct().count())

    # Run package code
    df = HitDetector().run(ais, tle)
    print("Length after processing:",df.count())
    # print(df.explain())
    df.write.saveAsTable('cmorris.af_vault_ais_tle_hit_scaled_test_1', mode='overwrite')

    print('Table successfully written to Hive')

if __name__ == "__main__":
    main()
