from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path

import pandas

from packages.utils.database_manager import DatabaseManager
from packages.utils.logger import Logger


class ETLBase(ABC):

    filesystem_path = os.path.join(os.getcwd(), "layers")

    @property
    @abstractmethod
    def layer(self):
        raise NotImplementedError("It is required to set 'layer' as class-level attribute.")

    @property
    @abstractmethod
    def entity_name(self):
        raise NotImplementedError("It is required to set 'entity_name' as class-level attribute.")

    def __init__(self):
        self._logger = Logger()
        self.__db_manager = DatabaseManager()

    def read_df_from_filesystem(self, path: str | None = None):
        if not path:
            path = os.path.join(self.filesystem_path, self.layer, f"{self.entity_name}.csv")
        self._logger.info(f"Reading file from: {path}")
        return pandas.read_csv(filepath_or_buffer=path, sep=',')

    def write_to_filesystem(self, df: pandas.DataFrame) -> None:
        self._logger.info(f"f: {self.filesystem_path}")
        self._logger.info(f"os: {os.getcwd()}")
        path = os.path.join(self.filesystem_path, self.layer, f"{self.entity_name}.csv")
        self._logger.info(f"Writing file to {path}")
        df.to_csv(path, sep=',', index=False)
        self._logger.info(f"File successfully saved.")

    def write_to_database(self, df: pandas.DataFrame, schema_name: str | None = None,
                          table_name: str | None = None) -> None:
        if not schema_name:
            schema_name = self.layer
        if not table_name:
            table_name = self.entity_name
        self._logger.info(f"Writing {table_name} table to {schema_name} schema")
        self.__db_manager.create_table_with_pandas_df(
            schema_name=schema_name,
            table_name=table_name,
            df=df
        )
        self._logger.info(f"Table successfully saved.")

    def write_to_fs_and_db(self, df: pandas.DataFrame, schema_name: str, table_name: str) -> None:
        self.write_to_filesystem(df=df)
        self.write_to_database(df=df, schema_name=schema_name, table_name=table_name)
