import unidecode
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, unix_timestamp, col, lower, udf
from pyspark.sql.types import StringType

from packages.etl.transformer import Transformer
import pandas


class ListaTarifasTransformer(Transformer):

    def __init__(self, spark: SparkSession):
        super().__init__(spark=spark, entity_name='lista_tarifas')

    def apply_transformation(self, df: pandas.DataFrame):
        self._logger.info("Normalizing columns names")
        lower_unidecode_udf = udf(lambda x: unidecode.unidecode(x.lower()), StringType())
        lista_tarifas_df = df
        lista_tarifas_df = lista_tarifas_df.withColumn("servico", lower(col("servico")))
        lista_tarifas_df = lista_tarifas_df.withColumn("tipo_valor", lower(col("tipo_valor")))
        lista_tarifas_df = lista_tarifas_df.withColumn("periodicidade", lower(col("periodicidade")))
        lista_tarifas_df = lista_tarifas_df.withColumn("unidade", lower_unidecode_udf("unidade"))
        lista_tarifas_df = lista_tarifas_df.withColumn('data_vigencia',
                                                       to_date(unix_timestamp(col('data_vigencia'), 'dd-MM-yyyy').cast(
                                                           "timestamp")))

        return lista_tarifas_df

    def execute(self):
        df = self._spark_session.read.parquet(f"{self.filesystem_path}/raw/lista_tarifas")
        df_transformed = self.apply_transformation(df=df)
        self._loader.write_to_filesystem(layer='trusted', df=df_transformed)
