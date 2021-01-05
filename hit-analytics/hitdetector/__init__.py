from pyspark.sql.window import Window
import pyspark.sql.functions as F

# Increment this version number when there is a new release:
__author__  = 'Christopher Morris'
__email__   = 'christopher.morris@jacobs.com'
__version__ = '0.1.0'


class HitDetector:
    def __init__(self):
        self.ais_groupby_cols = ['basedatetime']
        # self.message = "Hello world!"

    def run(self, ais, tle):
        if 'count' in ais.columns:
            ais = ais.drop('count')
        if 'count' in tle.columns:
            tle = tle.drop('count')

        

        ais = ais.repartition(100)
        tle = tle.repartition(200)

        period_of_validity = 14 # in days
        period_of_validity = period_of_validity * 24 * 60 * 60

        tle = tle.withColumn('ts_interval_start', tle['ts'] - period_of_validity)
        tle = tle.withColumn('ts_interval_end', tle['ts'] + period_of_validity)

        ais = ais.withColumn('ais_ts', F.unix_timestamp('basedatetime', format="yyyy-MM-dd'T'HH:mm:ss"))

        cond = [ais['ais_ts'] > tle['ts_interval_start'], ais['ais_ts'] < tle['ts_interval_end']]
        # jdf = ais.join(tle, ais['ts'].between(tle['ts_interval_start'], tle['ts_interval_end']))
        jdf = ais.join(tle, cond)
        # jdf.persist()

        jdf = jdf.withColumn('delta_t', F.abs(jdf['ais_ts'] - tle['ts']))

        columns = jdf.columns

        w = Window.partitionBy(*self.ais_groupby_cols,'satellite').orderBy('delta_t', 'line1')

        # jdf = jdf.select(*columns, F.min('delta_t').over(w).alias('min_delta_t'),
        #                            F.first('line1').over(w).alias('first_line1'))\
        #         .filter(F.col('delta_t')==F.col('min_delta_t'))\
        #         .filter(F.col('first_line1')==F.col('line1'))

        jdf = jdf.withColumn('index', F.row_number().over(w))
        jdf = jdf.filter(jdf['index']==1)

        # jdf = jdf.groupBy()

        # jdf.groupBy('imo','s')
        # jdf.cache()

        # jdf.count() # 442,526,950 if 14 days

        # jdf.show()

        return jdf
