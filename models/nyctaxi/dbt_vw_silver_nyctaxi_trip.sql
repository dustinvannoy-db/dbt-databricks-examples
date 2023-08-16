{{
 config(materialized = 'view',
 file_format = 'delta',
 persist_docs={"relation": true, "columns": true},
 tags="nyctaxi_sql")
}}

select
    *
    ,to_date(tpep_pickup_datetime, "yyyy-MM-dd HH:mm:ss") as pickup_timestamp
    ,to_date(tpep_dropoff_datetime, "yyyy-MM-dd HH:mm:ss") as dropoff_timestamp
from {{ref('dbt_vw_nyctaxi_trip')}}
