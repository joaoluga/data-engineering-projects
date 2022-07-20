import unidecode
import os
from packages.etl.transformer import Transformer


class BancosTransformer(Transformer):

    entity_name = 'bancos'

    def normalize_columns(self, df):
        col_list = df.columns.tolist()
        new_cols = {}
        for col in col_list:
            new_cols[col] = unidecode.unidecode(
                col.lower().replace("\x96", "").replace('-', '').replace('  ', '_').replace(' ', "_")).lower()
        df.rename(columns=new_cols, inplace=True)
        return df

    @staticmethod
    def normalize_indice(value):
        if value == ' ':
            return None
        else:
            return float(value.replace('.', '').replace(',', '.'))

    @staticmethod
    def normalize_to_int(value):
        if value == ' ':
            return 0
        else:
            return int(value)

    def apply_transformation(self):
        bancos_df = self.read_df_from_filesystem(
            os.path.join(self.filesystem_path, 'raw', f'{self.entity_name}.csv')
        )
        self._logger.info("Dropping not required columns")
        bancos_df.drop("Unnamed: 14", axis=1, inplace=True)
        self._logger.info("Normalizing columns names")
        bancos_df = self.normalize_columns(bancos_df)
        bancos_df['indice'] = bancos_df.indice.apply(self.normalize_indice)
        bancos_df['quantidade_total_de_clientes_ccs_e_scr'] = bancos_df.quantidade_total_de_clientes_ccs_e_scr.apply(
            self.normalize_to_int)
        bancos_df['quantidade_de_clientes_ccs'] = bancos_df.quantidade_de_clientes_ccs.apply(self.normalize_to_int)
        bancos_df['quantidade_de_clientes_scr'] = bancos_df.quantidade_de_clientes_scr.apply(self.normalize_to_int)
        bancos_df['categoria'] = bancos_df.categoria.apply(lambda x: x.lower())
        bancos_df['tipo'] = bancos_df.tipo.apply(lambda x: x.lower())
        bancos_df['instituicao_financeira'] = bancos_df.instituicao_financeira.apply(lambda x: x.lower())
        return bancos_df
