def model(dbt, session):
    dbt.config(materialized="table", tags=["python"])

    source_model_df = dbt.source("nyctaxi_hive_metastore", "yellow_json_vol_vw")

    final_df = source_model_df.selectExpr("*",
                "regexp_replace(substring(tpep_pickup_datetime,1,7), '-', '_') as pickup_date"
             )

    return final_df