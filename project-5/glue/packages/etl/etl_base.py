from __future__ import annotations

from abc import ABC, abstractmethod
from pyspark.sql import SparkSession

from packages.utils.logger import Logger
from packages.etl.loader import Loader


class ETLBase(ABC):

    def __init__(self, spark: SparkSession, entity_name: str | None = None, bucket_name: str | None = None,
                 conn_string: str | None = None):
        self._spark_session = spark
        self._logger = Logger()
        self.filesystem_path = f's3a://{bucket_name}/data_lake/layers'
        self.conn_string = conn_string
        self._loader = Loader(
            entity_name=entity_name,
            filesystem_path=self.filesystem_path)

    @abstractmethod
    def execute(self) -> None:
        pass
