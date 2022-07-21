SELECT
    bar.instituicao_financeira,
    MAX(foo.qtde_total_reclamacoes) as qtde_total_reclamacoes,
    MAX(foo.total_servicos) as total_servicos
FROM star_schema.fact_bancos_tarifas as foo
         JOIN star_schema.dim_instituicao_financeira as bar ON foo.instituicao_financeira_id = bar.instituicao_financeira_id
where
        foo.qtde_total_reclamacoes::decimal > 0
  AND bar.cnpj_if is not null
  AND total_servicos > 0
  AND bar.instituicao_financeira not ilike 'fact%%'
  AND bar.instituicao_financeira not ilike 'banco digio%%'
GROUP BY 1
ORDER BY 3 DESC
LIMIT 30


SELECT
    bar.instituicao_financeira,
    MAX(foo.total_taxas_gratuitas) as total_taxas_gratuitas
FROM star_schema.fact_bancos_tarifas as foo
         JOIN star_schema.dim_instituicao_financeira as bar ON foo.instituicao_financeira_id = bar.instituicao_financeira_id
where
        foo.qtde_total_reclamacoes::decimal > 0
  AND foo.qtde_total_reclamacoes::decimal < 1000
  AND bar.cnpj_if is not null
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10

SELECT
    bar.instituicao_financeira,
    SUM(foo.qtde_total_reclamacoes) as qtde_total_reclamacoes
FROM star_schema.fact_bancos_tarifas as foo
         JOIN star_schema.dim_instituicao_financeira as bar ON foo.instituicao_financeira_id = bar.instituicao_financeira_id
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10