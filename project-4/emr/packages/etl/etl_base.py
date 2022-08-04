from __future__ import annotations

from abc import ABC, abstractmethod

from pyspark.sql import SparkSession
from packages.utils.parameter_store_helper import get_parameter_value

from packages.utils.logger import Logger
from packages.etl.loader import Loader
import os


class ETLBase(ABC):

    filesystem_path = f's3a://{get_parameter_value("/emr/emr_bucket_name")}/data_lake/layers'

    def __init__(self, spark: SparkSession, entity_name: str | None = None):
        self._spark_session = spark
        self._logger = Logger()
        self._loader = Loader(
            entity_name=entity_name,
            filesystem_path=self.filesystem_path)

    @abstractmethod
    def execute(self) -> None:
        pass
