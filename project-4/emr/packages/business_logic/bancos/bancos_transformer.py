import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, FloatType
from packages.etl.transformer import Transformer
from pyspark.sql.functions import col, lower, udf


class BancosTransformer(Transformer):

    def __init__(self, spark: SparkSession):
        super().__init__(spark=spark, entity_name='bancos')

    @staticmethod
    def normalize_indice(value):
        if value == " ":
            return None
        else:
            return float(value.replace(".", "").replace(",", "."))

    @staticmethod
    def normalize_to_int(value):
        if value == " ":
            return 0
        else:
            return int(value)

    def apply_transformation(self, df: pyspark.sql.DataFrame):

        normalize_to_int_udf = udf(self.normalize_to_int, IntegerType())
        normalize_indice_udf = udf(self.normalize_indice, FloatType())
        bancos_df = df
        bancos_df = bancos_df.withColumn("indice", normalize_indice_udf("indice"))
        bancos_df = bancos_df.withColumn("quantidade_total_de_clientes_ccs_e_scr",
                                         normalize_to_int_udf("quantidade_total_de_clientes_ccs_e_scr"))
        bancos_df = bancos_df.withColumn("quantidade_de_clientes_ccs",
                                         normalize_to_int_udf("quantidade_de_clientes_ccs"))
        bancos_df = bancos_df.withColumn("quantidade_de_clientes_scr",
                                         normalize_to_int_udf("quantidade_de_clientes_scr"))
        bancos_df = bancos_df.withColumn("categoria", lower(col("categoria")))
        bancos_df = bancos_df.withColumn("tipo", lower(col("tipo")))
        bancos_df = bancos_df.withColumn("instituicao_financeira", lower(col("instituicao_financeira")))

        return bancos_df

    def execute(self):
        df = self._spark_session.read.parquet(f"{self.filesystem_path}/raw/bancos")
        df_transformed = self.apply_transformation(df=df)
        self._loader.write_to_filesystem(layer='trusted', df=df_transformed)

