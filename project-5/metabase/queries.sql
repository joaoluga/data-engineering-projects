-- top banks with more issues

SELECT
    replace(bar.instituicao_financeira, '(conglomerado)', '') as instituicao_financeira,
    SUM(foo.qtde_total_reclamacoes) as qtde_total_reclamacoes
FROM project5_refined.fact_bancos_tarifas as foo
         JOIN project5_refined.dim_instituicao_financeira as bar ON foo.instituicao_financeira_id = bar.instituicao_financeira_id
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10

-- top banks with more free services

SELECT
    replace(replace(replace(replace(bar.instituicao_financeira, 's.a', ''), 'banco', ''), 'credito, financiamento e investimento', ''), 'crédito, financiamento e investimento', '') as instituicao_financeira,
    MAX(foo.total_taxas_gratuitas) as total_taxas_gratuitas
FROM project5_refined.fact_bancos_tarifas as foo
         JOIN project5_refined.dim_instituicao_financeira as bar ON foo.instituicao_financeira_id = bar.instituicao_financeira_id
where
      foo.qtde_total_reclamacoes > 0
  AND foo.qtde_total_reclamacoes < 1000
  AND bar.cnpj_if is not null
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10

-- total_services x total_issues

SELECT
    replace(replace(replace(replace(bar.instituicao_financeira, 's.a', ''), 'banco', ''), 'credito, financiamento e investimento', ''), 'crédito, financiamento e investimento', '') as instituicao_financeira,
    MAX(foo.qtde_total_reclamacoes) as qtde_total_reclamacoes,
    MAX(foo.total_servicos) as total_servicos
FROM project5_refined.fact_bancos_tarifas as foo
         JOIN project5_refined.dim_instituicao_financeira as bar ON foo.instituicao_financeira_id = bar.instituicao_financeira_id
where
        foo.qtde_total_reclamacoes > 0
  AND bar.cnpj_if is not null
  AND total_servicos > 0
  AND bar.instituicao_financeira not like 'fact%'
  AND bar.instituicao_financeira not like 'banco digio%'
GROUP BY 1
ORDER BY 3 DESC
LIMIT 30