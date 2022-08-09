from pyspark.sql import SparkSession
from packages.etl.etl_factory import ETLFactory
import sys
from awsglue.utils import getResolvedOptions


args = getResolvedOptions(sys.argv,
                          ['JOB_NAME',
                           'entity_name',
                           'etl_phase',
                           'bucket_name'])


etl_class = ETLFactory(
    entity_name=args['entity_name'],
    process=args['etl_phase']
).get_etl_class()

spark = SparkSession.builder.getOrCreate()
etl_class(
    spark=spark,
    bucket_name=args['bucket_name'],
    conn_string=None
).execute()
