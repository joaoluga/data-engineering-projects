
SELECT
    DISTINCT md5(categoria) as categoria_id, categoria
FROM {{ source('trusted', 'bancos') }}
