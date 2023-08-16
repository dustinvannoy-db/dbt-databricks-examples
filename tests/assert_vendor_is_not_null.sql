{{ config(store_failures = true) }}

select *
from {{ref('dbt_silver_nyctaxi_trip')}}
where VendorID is null