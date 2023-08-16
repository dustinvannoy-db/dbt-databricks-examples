{{
 config(materialized = 'view', 
 persist_docs={"relation": true, "columns": true})
}}

select
  *,
  'yellow_json' as source
from json.`{{ var("source_volume_base_path") }}/source/tripdata/yellow_json`