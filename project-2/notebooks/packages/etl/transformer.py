from abc import abstractmethod
import pandas

from packages.etl.etl_base import ETLBase


class Transformer(ETLBase):

    layer = 'trusted'

    def __init__(self):
        super().__init__()

    @abstractmethod
    def apply_transformation(self) -> pandas.DataFrame:
        pass

    def execute(self):
        df = self.apply_transformation()
        self.write_to_filesystem(df)