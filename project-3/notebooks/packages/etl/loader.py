from __future__ import annotations
from abc import abstractmethod
from packages.utils.database_manager import DatabaseManager
from packages.etl.etl_base import ETLBase
import pandas
import os


class Loader(ETLBase):
    @property
    @abstractmethod
    def entity_name(self):
        raise NotImplementedError(
            "It is required to set 'entity_name' as class-level attribute."
        )

    def __init__(self) -> None:
        self.__db_manager = DatabaseManager()
        super().__init__()

    def write_to_filesystem(self, layer: str, df: pandas.DataFrame) -> None:
        path = os.path.join(self.filesystem_path, layer, f"{self.entity_name}.csv")
        self._logger.info(f"Writing file to {path}")
        df.to_csv(path, sep=",", index=False)
        self._logger.info(f"File successfully saved.")

    def write_to_database(
        self,
        df: pandas.DataFrame,
        schema_name: str | None = None,
        table_name: str | None = None,
    ) -> None:
        if not table_name:
            table_name = self.entity_name
        self._logger.info(f"Writing {table_name} table to {schema_name} schema")
        self.__db_manager.create_table_with_pandas_df(
            schema_name=schema_name, table_name=table_name, df=df
        )
        self._logger.info(f"Table successfully saved.")
