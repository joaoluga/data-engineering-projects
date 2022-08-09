from __future__ import annotations

from abc import abstractmethod
import pandas
import pyspark.sql
from pyspark.sql import SparkSession

from packages.etl.etl_base import ETLBase


class Transformer(ETLBase):
    def __init__(self, spark: SparkSession, entity_name: str | None = None, bucket_name: str | None = None,
                 conn_string: str | None = None):
        super().__init__(spark=spark, entity_name=entity_name, bucket_name=bucket_name, conn_string=conn_string)

    @abstractmethod
    def apply_transformation(self, df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        pass