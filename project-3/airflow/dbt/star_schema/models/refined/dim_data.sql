

SELECT DISTINCT
    md5(CONCAT(ano, trimestre)) as data_id,
    ano, trimestre
FROM {{ source('trusted', 'bancos') }}