spark-submit --driver-memory 12g --executor-memory 12g --executor-cores 2  --conf spark.kryoserializer.buffer.max=128m --conf spark.driver.maxResultSize=2g --py-files simpleKml.zip 1-HivetoKml.py 
