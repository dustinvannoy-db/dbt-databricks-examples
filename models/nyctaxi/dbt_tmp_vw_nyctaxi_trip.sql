-- Example using s3 directly instead of volume
{{
 config(materialized = 'ephemeral')
}}

select
  *,
  'yellow_json' as source
from {{ source('nyctaxi_hive_metastore', 'yellow_json_vw')}}