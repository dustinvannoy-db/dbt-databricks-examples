{{ config(store_failures = true) }}

select VendorId, sum(fare_amount) TotalFareAmount
from {{ref('dbt_silver_nyctaxi_trip')}}
group by VendorId 
having sum(fare_amount) < 0