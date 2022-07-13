-- Star Schema Creation
CREATE SCHEMA IF NOT EXISTS star_schema;

-- Categoria Dim Creation
DROP TABLE IF EXISTS star_schema.categoria_dim;
CREATE TABLE star_schema.categoria_dim as
SELECT DISTINCT md5(categoria) as categoria_id, categoria  FROM bancos;

-- Tipo Dim Creation
DROP TABLE IF EXISTS star_schema.tipo_dim;
CREATE TABLE star_schema.tipo_dim as
SELECT DISTINCT md5(tipo) as tipo_id, tipo  FROM bancos;

-- Instituicao Financeira Dim Creation
DROP TABLE IF EXISTS star_schema.instituicao_financeira_dim;
CREATE TABLE star_schema.instituicao_financeira_dim as
SELECT DISTINCT md5(CONCAT(cnpj, instituicao_financeira)) as instituicao_financeira_id, cnpj, instituicao_financeira, indice  FROM bancos;

-- Data Dim Creation
DROP TABLE IF EXISTS star_schema.data_dim;
CREATE TABLE star_schema.data_dim as
SELECT DISTINCT md5(CONCAT(ano, trimestre)) as data_id, ano, trimestre FROM bancos;

-- Banco Tarifa Fact Creation
DROP TABLE IF EXISTS star_schema.bancos_tarifa_fact;
CREATE TABLE star_schema.bancos_tarifa_fact as
SELECT
    bar.id,
    bar.created_at,
    md5(CONCAT(bar.ano, bar.trimestre)) as data_id,
    md5(CONCAT(bar.cnpj, bar.instituicao_financeira)) as instituicao_financeira_id,
    md5(bar.categoria) as categoria,
    md5(bar.tipo) as tipo,
    CASE WHEN bar.qtde_reclamacoes_reguladas_procedentes = ' ' THEN 0 ELSE bar.qtde_reclamacoes_reguladas_procedentes::decimal END qtde_reclamacoes_reguladas_procedentes,
    CASE WHEN bar.qtde_reclamacoes_reguladas_outras = ' ' THEN 0 ELSE bar.qtde_reclamacoes_reguladas_outras::decimal END qtde_reclamacoes_reguladas_outras,
    CASE WHEN bar.qtde_de_reclamacoes_nao_reguladas = ' ' THEN 0 ELSE bar.qtde_de_reclamacoes_nao_reguladas::decimal END qtde_de_reclamacoes_nao_reguladas,
    CASE WHEN bar.qtde_total_reclamacoes = ' ' THEN 0 ELSE bar.qtde_total_reclamacoes::decimal END qtde_total_reclamacoes,
    CASE WHEN bar.qtde_total_clientes_spa_ccs_e_scr = ' ' THEN 0 ELSE bar.qtde_total_clientes_spa_ccs_e_scr::decimal END qtde_total_clientes_spa_ccs_e_scr,
    CASE WHEN bar.qtde_clientes_spa_ccs = ' ' THEN 0 ELSE bar.qtde_clientes_spa_ccs::decimal END qtde_clientes_spa_ccs,
    CASE WHEN bar.qtde_clientes_spa_scr = ' ' THEN 0 ELSE bar.qtde_clientes_spa_scr::decimal END qtde_clientes_spa_scr,
    coalesce(foo.total_servicos, 0) as total_servicos,
    coalesce(foo.total_cobrancas_type, 0) as total_cobrancas_type,
    coalesce(foo.total_taxas_pagas, 0) as total_taxas_pagas,
    coalesce(foo.total_taxas_gratuitas, 0) as total_taxas_gratuitas,
    coalesce(foo.valor_maximo_taxa_real, 0) as valor_maximo_taxa_real,
    coalesce(foo.valor_maximo_taxa_percentual, 0) as valor_maximo_taxa_percentual
FROM bancos as bar
         LEFT JOIN
     (SELECT
          cnpj,
          COUNT(DISTINCT servico) as total_servicos,
          COUNT(DISTINCT periodicidade) as total_cobrancas_type,
          COUNT(DISTINCT servico) - COUNT(DISTINCT CASE WHEN valor_maximo::decimal = 0 THEN servico ELSE NULL END) as total_taxas_pagas,
          COUNT(DISTINCT CASE WHEN valor_maximo::decimal = 0 THEN servico ELSE NULL END) as total_taxas_gratuitas,
          MAX(CASE WHEN Tipo_valor = 'Real' THEN valor_maximo::decimal ELSE 0 END) as valor_maximo_taxa_real,
          MAX(CASE WHEN Tipo_valor = 'Percentual' THEN valor_maximo::decimal ELSE 0 END) as valor_maximo_taxa_percentual
      FROM lista_tarifas
      GROUP BY 1) as foo ON foo.cnpj = bar.cnpj