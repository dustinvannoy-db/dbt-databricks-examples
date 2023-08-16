{{ config(store_failures = true) }}

-- notes: quarantine records and isolate them if the total  amount is negative -- 
select *
from {{ref('dbt_silver_nyctaxi_trip')}}
where PULocationID is null