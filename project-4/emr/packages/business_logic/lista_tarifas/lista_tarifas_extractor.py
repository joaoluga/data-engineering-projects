import re

from pyspark.sql import SparkSession
from unidecode import unidecode

from packages.etl.rest_api_extractor import RestApiExtractor
from multiprocessing import Process, Manager
import pandas
import time
import os


class ListaTarifasExtractor(RestApiExtractor):

    endpoint = (
        "https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/"
        "odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ="
        "@CNPJ)?@PessoaFisicaOuJuridica='J'&@CNPJ='{cnpj}'&$top=100&$format=json&$select=CodigoServico,"
        "Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
    )

    def __init__(self, spark: SparkSession):
        super().__init__(spark=spark, entity_name='lista_tarifas')

    @staticmethod
    def normalize_columns(df):
        col_list = df.columns.tolist()
        new_cols = {}
        for col in col_list:
            matches = re.finditer(
                ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", col
            )
            col_name = "_".join([m.group(0) for m in matches]).lower()
            new_cols[col] = unidecode(col_name)
        df.rename(columns=new_cols, inplace=True)
        df.drop(columns=["@odata.context"], inplace=True)
        return df

    def get_lista_tarifas_df(self, url, cnpj, raw_data):
        result = self._api_hook.get(endpoint=url, headers=None, output_type="json")
        result["cnpj"] = cnpj
        raw_data.append(result)

    def get_data(self) -> pandas.DataFrame:
        start_time = time.perf_counter()
        manager = Manager()
        raw_data = manager.list()
        processes = []
        bancos_df = pandas.read_parquet(
            os.path.join(self.filesystem_path, "raw/bancos")
        )
        cnpj_list = (
            bancos_df["cnpj_if"].replace(" ", None).dropna().drop_duplicates().tolist()
        )
        for cnpj in cnpj_list:
            url = self.endpoint.format(cnpj=cnpj)
            t = Process(target=self.get_lista_tarifas_df, args=(url, cnpj, raw_data))
            t.start()
            processes.append(t)
        for process in processes:
            process.join()
        finish_time = time.perf_counter()
        self._logger.info(f"Report retrieved in {finish_time-start_time} seconds")
        return pandas.json_normalize(
            list(raw_data), "value", ["@odata.context", "cnpj"]
        )

    def execute(self):
        pandas_df = self.get_data()
        pandas_df = self.normalize_columns(pandas_df)
        df = self.convert_to_sparkdataframe(pandas_df)
        self._loader.write_to_filesystem(layer='raw', df=df)
