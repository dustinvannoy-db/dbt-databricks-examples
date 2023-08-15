{{
 config(materialized = 'table', file_format = 'delta', persist_docs={"relation": true, "columns": true})
}}

select
    pickup_date
    ,count(1) as trips
    ,sum(total_amount) amount
    --,sum(trip_distance) total_distance
from {{ref('dbt_silver_nyctaxi_trip')}}
group by pickup_date