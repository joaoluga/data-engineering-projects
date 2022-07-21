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

    def __init_(self):
        super().__init__()

    def get_lista_tarifas_df(self, url, cnpj, raw_data):
        result = self._api_hook.get(endpoint=url, headers=None, output_type="json")
        result["cnpj"] = cnpj
        raw_data.append(result)

    def get_data(self) -> pandas.DataFrame:
        start_time = time.perf_counter()
        manager = Manager()
        raw_data = manager.list()
        processes = []
        bancos_df = pandas.read_csv(
            os.path.join(self.filesystem_path, "trusted/bancos.csv")
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
