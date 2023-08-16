{{config(materialized = 'materialized_view', tags=["nyctaxi_sql"])}}

select
    pickup_date
    ,count(1) as trips
    ,sum(total_amount) amount
from {{ref('dbt_silver_nyctaxi_trip')}}
group by pickup_date