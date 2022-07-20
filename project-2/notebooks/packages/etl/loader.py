from packages.etl.etl_base import ETLBase


class Loader(ETLBase):

    layer = 'trusted'

    def __init__(self):
        super().__init__()

    def execute(self):
        df = self.read_df_from_filesystem()
        self.write_to_database(df=df)
