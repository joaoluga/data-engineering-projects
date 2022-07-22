from multiprocessing import Process, Manager
import pandas
import time
from io import StringIO

from packages.etl.rest_api_extractor import RestApiExtractor


class BancosExtractor(RestApiExtractor):
    # https://dados.gov.br/dataset/ranking-de-instituicoes-por-indice-de-reclamacoes

    endpoint = (
        "https://www3.bcb.gov.br/rdrweb/rest/ext/ranking/arquivo?ano={ano}&periodicidade=TRIMESTRAL&periodo"
        "={periodo}&tipo=Bancos%20e%20financeiras"
    )
    period = {
        "20201": (2020, 1),
        "20202": (2020, 2),
        "20203": (2020, 3),
        "20204": (2020, 4),
        "20211": (2021, 1),
        "20212": (2021, 2),
        "20213": (2021, 3),
        "20214": (2021, 4),
    }

    def __init__(self):
        super().__init__()

    def get_bancos_df(self, url, raw_data):
        result = self._api_hook.get(
            endpoint=url, headers=None, output_type="text", encoding="latin-1"
        )
        len(result)
        data = StringIO(result)
        raw_data.append(pandas.read_csv(data, sep=";"))

    def get_data(self) -> pandas.DataFrame:
        start_time = time.perf_counter()
        manager = Manager()
        raw_data = manager.list()
        processes = []
        for item in self.period.values():
            url = self.endpoint.format(
                ano=item[0],
                periodo=item[1],
            )
            t = Process(target=self.get_bancos_df, args=(url, raw_data))
            t.start()
            processes.append(t)
        for process in processes:
            process.join()
        finish_time = time.perf_counter()
        self._logger.info(f"Report retrieved in {finish_time - start_time} seconds")
        return pandas.concat(raw_data)
