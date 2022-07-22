import unidecode
import os
from packages.etl.transformer import Transformer
import re
import pandas


class ListaTarifasTransformer(Transformer):
    @staticmethod
    def normalize_columns(df):
        col_list = df.columns.tolist()
        new_cols = {}
        for col in col_list:
            matches = re.finditer(
                ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", col
            )
            col_name = "_".join([m.group(0) for m in matches]).lower()
            new_cols[col] = unidecode.unidecode(col_name)
        df.rename(columns=new_cols, inplace=True)
        return df

    def apply_transformation(self, df: pandas.DataFrame):
        self._logger.info("Dropping not required columns")
        df.drop(columns=["@odata.context"], inplace=True)
        self._logger.info("Normalizing columns names")
        lista_tarifas_df = ListaTarifasTransformer.normalize_columns(df)
        lista_tarifas_df["servico"] = lista_tarifas_df.servico.apply(
            lambda x: x.lower()
        )
        lista_tarifas_df["unidade"] = lista_tarifas_df.unidade.apply(
            lambda x: unidecode.unidecode(x.lower())
        )
        lista_tarifas_df["data_vigencia"] = pandas.to_datetime(
            lista_tarifas_df.data_vigencia
        )
        lista_tarifas_df["tipo_valor"] = lista_tarifas_df.tipo_valor.apply(
            lambda x: x.lower()
        )
        lista_tarifas_df["periodicidade"] = lista_tarifas_df.periodicidade.apply(
            lambda x: x.lower()
        )
        return lista_tarifas_df
