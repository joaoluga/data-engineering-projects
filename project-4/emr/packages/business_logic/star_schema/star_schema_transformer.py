from __future__ import annotations

import pyspark

from packages.etl.transformer import Transformer
from packages.utils.parameter_store_helper import get_parameter_value


class StarSchemaTransformer(Transformer):

    def create_table_as_query(self, layer_name, table_name, conn_string, query, partitions):
        self._logger.info(f"Creating {layer_name}.{table_name}")
        df = self._spark_session.sql(query)
        self._loader.entity_name = table_name
        self._logger.info("Writing to database")
        self._loader.write_to_database(
            conn_string=conn_string,
            df=df.toPandas(),
            schema_name=layer_name)
        self._logger.info("Writing to DataLake")
        self._loader.write_to_filesystem(layer=layer_name, df=df, partitions=partitions)

    def apply_transformation(self, df: pyspark.sql.DataFrame | None) -> None:

        layer_name = 'refined'
        conn_string_ssm = get_parameter_value('/rds/analytics-db-dev/sqlalchemy_conn')
        conn_string = conn_string_ssm.replace("+psycopg2", "")
        self.create_table_as_query(
            layer_name=layer_name,
            table_name='dim_categoria',
            conn_string=conn_string,
            query="SELECT DISTINCT md5(categoria) as categoria_id, categoria  FROM trusted_bancos",
            partitions=['categoria']
        )

        self.create_table_as_query(
            layer_name=layer_name,
            table_name='dim_tipo',
            conn_string=conn_string,
            query="SELECT DISTINCT md5(tipo) as tipo_id, tipo  FROM trusted_bancos",
            partitions=['tipo']
        )

        self.create_table_as_query(
            layer_name=layer_name,
            table_name='dim_instituicao_financeira',
            conn_string=conn_string,
            query="SELECT DISTINCT md5(CONCAT(cnpj_if, "
                  "instituicao_financeira)) as instituicao_financeira_id, "
                  "cnpj_if, instituicao_financeira, indice  "
                  "FROM trusted_bancos",
            partitions=['instituicao_financeira_id']
        )

        self.create_table_as_query(
            layer_name=layer_name,
            table_name='dim_data',
            conn_string=conn_string,
            query="SELECT DISTINCT md5(CONCAT(ano, trimestre)) as data_id, ano, trimestre "
                  "FROM trusted_bancos",
            partitions=['ano']
        )

        self.create_table_as_query(
            layer_name=layer_name,
            table_name='fact_bancos_tarifas',
            conn_string=conn_string,
            partitions=['groups'],
            query="""
                SELECT
                    md5(CONCAT(bar.ano, bar.trimestre)) as data_id,
                    md5(CONCAT(bar.cnpj_if, bar.instituicao_financeira)) as instituicao_financeira_id,
                    md5(bar.categoria) as categoria,
                    md5(bar.tipo) as tipo,
                    cast(bar.quantidade_de_reclamacoes_reguladas_procedentes as float) as  quantidade_de_reclamacoes_reguladas_procedentes,
                    cast(bar.quantidade_de_reclamacoes_reguladas_outras as float) as qtde_reclamacoes_reguladas_outras,
                    cast(bar.quantidade_de_reclamacoes_nao_reguladas as float) as qtde_de_reclamacoes_nao_reguladas,
                    cast(bar.quantidade_total_de_reclamacoes as float) as  qtde_total_reclamacoes,
                    cast(bar.quantidade_total_de_clientes_ccs_e_scr as float) as qtde_total_clientes_spa_ccs_e_scr,
                    cast(bar.quantidade_de_clientes_ccs as float) as qtde_clientes_spa_ccs,
                    cast(bar.quantidade_de_clientes_scr as float) as qtde_clientes_spa_scr,
                    coalesce(foo.total_servicos, 0) as total_servicos,
                    coalesce(foo.total_cobrancas_type, 0) as total_cobrancas_type,
                    coalesce(foo.total_taxas_pagas, 0) as total_taxas_pagas,
                    coalesce(foo.total_taxas_gratuitas, 0) as total_taxas_gratuitas,
                    coalesce(foo.valor_maximo_taxa_real, 0) as valor_maximo_taxa_real,
                    coalesce(foo.valor_maximo_taxa_percentual, 0) as valor_maximo_taxa_percentual,
                    CASE 
                        WHEN cast(quantidade_total_de_reclamacoes as float) < 10 THEN '10'
                        WHEN cast(quantidade_total_de_reclamacoes as float) < 100 THEN '100'
                        WHEN cast(quantidade_total_de_reclamacoes as float) <= 400 THEN '400'
                        WHEN cast(quantidade_total_de_reclamacoes as float) >= 401 THEN '401'
                    END as groups
                FROM trusted_bancos as bar
                    LEFT JOIN
                        (SELECT
                            cnpj,
                            COUNT(DISTINCT servico) as total_servicos,
                            COUNT(DISTINCT periodicidade) as total_cobrancas_type,
                            (COUNT(DISTINCT servico) - COUNT(DISTINCT IF(cast(valor_maximo as float) = 0, servico, NULL))) as total_taxas_pagas,
                            COUNT(DISTINCT IF(cast(valor_maximo as float) = 0, servico, NULL)) as total_taxas_gratuitas,
                            MAX(IF(Tipo_valor = 'Real', cast(valor_maximo as float), 0)) as valor_maximo_taxa_real,
                            MAX(IF(Tipo_valor = 'Percentual', cast(valor_maximo as float), 0))  as valor_maximo_taxa_percentual
                        FROM trusted_lista_tarifas
                        GROUP BY 1) as foo ON cast(foo.cnpj as string) = bar.cnpj_if""")

    def execute(self) -> None:
        df_bancos = self._spark_session.read.parquet(f"{self.filesystem_path}/trusted/bancos")
        df_bancos.registerTempTable("trusted_bancos")
        df_lt = self._spark_session.read.parquet(f"{self.filesystem_path}/trusted/lista_tarifas")
        df_lt.registerTempTable("trusted_lista_tarifas")
        self.apply_transformation(None)

