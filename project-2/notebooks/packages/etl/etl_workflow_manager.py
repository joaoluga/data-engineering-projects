import pandas

from packages.etl.etl_base import ETLBase
from packages.etl.etl_factory import ETLFactory


class ETLWorkflowManager(ETLBase):
    def __init__(self, entity_name):
        self.extractor_cls, self.transformer_cls, self.loader_cls = ETLFactory(
            entity_name=entity_name
        ).get_etl_classes()
        self.extractor = self.extractor_cls()
        self.transformer = self.transformer_cls()
        self.loader = self.loader_cls()
        super().__init__()

    def extract(self) -> pandas.DataFrame:
        self._logger.info("Starting Extraction process")
        extract_df = self.extractor.get_data()
        self._logger.info("Writing extract result to raw layer")
        self.loader.write_to_filesystem("raw", extract_df)
        return extract_df

    def transform(self, df: pandas.DataFrame) -> pandas.DataFrame:
        self._logger.info("Starting Transformation process")
        transformed_df = self.transformer.apply_transformation(df=df)
        self._logger.info("Writing Transformation result to trusted layer")
        self.loader.write_to_filesystem("trusted", transformed_df)
        return transformed_df

    def load(self, df: pandas.DataFrame) -> None:
        self._logger.info("Writing Transformation result database")
        return self.loader.write_to_database(df=df, schema_name="trusted")

    def execute(self):
        extract_df = self.extract()
        transformed_df = self.transform(extract_df)
        self.load(transformed_df)
