{{
 config(materialized = 'streaming_table',
 tblproperties = {'delta.enableChangeDataFeed': 'true'},
 file_format = 'delta',
 persist_docs={"relation": true, "columns": true},
 tags="nyctaxi_sql")
}}

select
  *,
  regexp_replace(substring(tpep_pickup_datetime, 1, 7), '-', '_') as pickup_date,
  'yellow_json' as source
from stream read_files(
    '{{ var("source_volume_base_path") }}/source/tripdata/yellow/'
  )