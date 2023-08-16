from pyspark.sql.functions import lit
# from databricks_with_poetry.misc_functions import id_lookup

def model(dbt, session):
    dbt.config(materialized="incremental", tags=["python"])
    
    upstream_df = dbt.ref("dbt_bronze_nyctaxi_pytrip")

    if dbt.is_incremental:
        max_loaded_sql = f"select max(pickup_date) from {dbt.this}"
        upstream_df.filter(upstream_df.pickup_date > session.sql(max_loaded_sql).collect()[0][0])

    final_df = upstream_df.selectExpr("*",
                'to_date(tpep_pickup_datetime, "yyyy-MM-dd HH:mm:ss") as pickup_timestamp',
                'to_date(tpep_dropoff_datetime, "yyyy-MM-dd HH:mm:ss") as dropoff_timestamp'
             )
    
    # Uncomment next line to use custom library
    # final_df = final_df.withColumn("person_id", lit(id_lookup('person1')))

    return final_df