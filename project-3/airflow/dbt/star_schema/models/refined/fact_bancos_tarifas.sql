SELECT
    bar.index,
    md5(CONCAT(bar.ano, bar.trimestre)) as data_id,
    md5(CONCAT(bar.cnpj_if, bar.instituicao_financeira)) as instituicao_financeira_id,
    md5(bar.categoria) as categoria,
    md5(bar.tipo) as tipo,
    bar.quantidade_de_reclamacoes_reguladas_procedentes as
        quantidade_de_reclamacoes_reguladas_procedentes,
    bar.quantidade_de_reclamacoes_reguladas_outras as qtde_reclamacoes_reguladas_outras,
    bar.quantidade_de_reclamacoes_nao_reguladas as qtde_de_reclamacoes_nao_reguladas,
    bar.quantidade_total_de_reclamacoes as  qtde_total_reclamacoes,
    bar.quantidade_total_de_clientes_ccs_e_scr as qtde_total_clientes_spa_ccs_e_scr,
    bar.quantidade_de_clientes_ccs as qtde_clientes_spa_ccs,
    bar.quantidade_de_clientes_scr as qtde_clientes_spa_scr,
    coalesce(foo.total_servicos, 0) as total_servicos,
    coalesce(foo.total_cobrancas_type, 0) as total_cobrancas_type,
    coalesce(foo.total_taxas_pagas, 0) as total_taxas_pagas,
    coalesce(foo.total_taxas_gratuitas, 0) as total_taxas_gratuitas,
    coalesce(foo.valor_maximo_taxa_real, 0) as valor_maximo_taxa_real,
    coalesce(foo.valor_maximo_taxa_percentual, 0) as valor_maximo_taxa_percentual
FROM {{ source('trusted', 'bancos') }} as bar
         LEFT JOIN
     (SELECT
          cnpj,
          COUNT(DISTINCT servico) as total_servicos,
          COUNT(DISTINCT periodicidade) as total_cobrancas_type,
          COUNT(DISTINCT servico) - COUNT(DISTINCT CASE WHEN valor_maximo::decimal = 0
                                                            THEN servico ELSE NULL END) as total_taxas_pagas,
          COUNT(DISTINCT CASE WHEN valor_maximo::decimal = 0 THEN servico ELSE NULL END)
              as total_taxas_gratuitas,
          MAX(CASE WHEN Tipo_valor = 'Real' THEN valor_maximo::decimal ELSE 0 END)
              as valor_maximo_taxa_real,
          MAX(CASE WHEN Tipo_valor = 'Percentual' THEN valor_maximo::decimal ELSE 0 END)
              as valor_maximo_taxa_percentual
      FROM {{ source('trusted', 'lista_tarifas') }}
      GROUP BY 1) as foo ON foo.cnpj::varchar = bar.cnpj_if