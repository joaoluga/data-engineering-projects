from abc import abstractmethod
import pandas

from packages.etl.etl_base import ETLBase


class Transformer(ETLBase):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def apply_transformation(self, df: pandas.DataFrame) -> pandas.DataFrame:
        pass
