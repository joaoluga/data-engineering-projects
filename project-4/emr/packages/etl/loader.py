from __future__ import annotations

import pandas
import pyspark
import os

from packages.utils.database_manager import DatabaseManager
from packages.utils.logger import Logger


class Loader:

    def __init__(self, entity_name, filesystem_path) -> None:
        self.entity_name = entity_name
        self.filesystem_path = filesystem_path
        self._logger = Logger()
        super().__init__()

    def write_to_filesystem(self, layer: str, df: pyspark.sql.DataFrame, partitions: list | None = None,
                            mode: str = 'overwrite') -> None:
        if partitions is None:
            partitions = []
        path = os.path.join(self.filesystem_path, layer, self.entity_name)
        self._logger.info(f"Writing file to {path}")
        df.write.partitionBy(*partitions).mode(mode).parquet(path)
        self._logger.info(f"File successfully saved.")

    def write_to_database(self, conn_string: str, df: pandas.DataFrame, schema_name: str = 'public') -> None:
        self._logger.info("Connecting to Database")
        db_manager = DatabaseManager(conn_string=conn_string)
        db_manager.create_schema(schema_name=schema_name)
        self._logger.info(f"Writing {self.entity_name} to schema {self.entity_name}")
        db_manager.create_table_with_pandas_df(
            df=df,
            table_name=self.entity_name,
            schema_name=schema_name
        )
