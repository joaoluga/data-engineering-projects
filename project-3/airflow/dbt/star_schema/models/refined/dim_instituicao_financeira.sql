

SELECT DISTINCT
    md5(CONCAT(cnpj_if, instituicao_financeira)) as instituicao_financeira_id,
    cnpj_if,
    instituicao_financeira,
    indice
FROM {{ source('trusted', 'bancos') }}