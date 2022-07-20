from abc import abstractmethod

import pandas

from packages.etl.etl_base import ETLBase
from packages.utils.rest_api_hook import RestApiHook


class RestApiExtractor(ETLBase):

    layer = "raw"

    @property
    @abstractmethod
    def endpoint(self):
        raise NotImplementedError("It is required to set 'endpoint' as class-level attribute.")

    def __init__(self):
        self._api_hook = RestApiHook()
        super().__init__()

    @abstractmethod
    def get_data(self) -> pandas.DataFrame:
        raise NotImplementedError("It is required to set 'get_report' method")

    def execute(self):
        df = self.get_data()
        self.write_to_filesystem(df)

