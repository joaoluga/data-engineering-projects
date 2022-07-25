
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

SELECT
    DISTINCT md5(categoria) as categoria_id, categoria
FROM {{ source('trusted', 'bancos') }}
