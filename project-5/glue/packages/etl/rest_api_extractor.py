from __future__ import annotations

from abc import abstractmethod

import pandas
from pyspark.sql import SparkSession
from pyspark.sql.types import TimestampType, LongType, IntegerType, DoubleType, FloatType, StringType, StructField, \
    StructType

from packages.etl.etl_base import ETLBase
from packages.utils.rest_api_hook import RestApiHook


class RestApiExtractor(ETLBase):

    @property
    @abstractmethod
    def endpoint(self):
        raise NotImplementedError(
            "It is required to set 'endpoint' as class-level attribute."
        )

    df_spark_types = {
        'datetime64[ns]': TimestampType(),
        'int64': LongType(),
        'int32': IntegerType(),
        'float64': DoubleType(),
        'float32': FloatType(),
        'object': StringType()
    }

    def __init__(self, spark: SparkSession, entity_name: str | None = None, bucket_name: str | None = None,
                 conn_string: str | None = None):
        self._api_hook = RestApiHook()
        super().__init__(spark=spark, entity_name=entity_name, bucket_name=bucket_name, conn_string=conn_string)

    def generate_schema(self, string, format_type):
        try:
            spark_type = self.df_spark_types[format_type]
        except Exception:
            spark_type = StringType()
        return StructField(string, spark_type)

    def convert_to_sparkdataframe(self, pandas_df):
        columns = list(pandas_df.columns)
        types = list(pandas_df.dtypes)
        struct_list = []
        for column, typo in zip(columns, types):
            struct_list.append(self.generate_schema(column, typo))
        schema = StructType(struct_list)
        return self._spark_session.createDataFrame(pandas_df, schema)

    @abstractmethod
    def get_data(self) -> pandas.DataFrame:
        raise NotImplementedError("It is required to set 'get_report' method")
