{{ config(store_failures = true) }}

-- notes: quarantine records and isolate them if the total sales amount is negative -- 
select VendorId, sum(fare_amount) TotalFareAmount
from {{ref('dbt_silver_nyctaxi_trip')}}
group by VendorId 
having sum(fare_amount) < 0