

SELECT
    DISTINCT md5(tipo) as tipo_id, tipo
FROM {{ source('trusted', 'bancos') }}
