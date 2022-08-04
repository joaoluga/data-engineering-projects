from pyspark.sql import SparkSession
from packages.etl.etl_factory import ETLFactory
import sys

entity_name = sys.argv[1]
etl_phase = sys.argv[2]
bucket_name = sys.argv[3]


etl_class = ETLFactory(
    entity_name=entity_name,
    process=etl_phase
).get_etl_class()

spark = SparkSession.builder.getOrCreate()
etl_class(spark=spark).execute()
