# Databricks notebook source
# MAGIC %md
# MAGIC # DBT Runner
# MAGIC Use this notebook to run DBT Databricks models from within the same Databricks Repo. See the profiles.yml that is stored in the same repo as this notebook and relies on environment variables.
# MAGIC 1. Set Databricks Secrets for HOST, TOKEN, HTTP_PATH (warehouse). Modify command 5 to pull correct secrets for your testing.
# MAGIC 2. Choose Catalog and Schema for dbt to use when writing
# MAGIC 3. Selection Logic
# MAGIC   1. Leave empty to run all models. Otherwise provide a model name or other valid [dbt select clause](https://docs.getdbt.com/reference/node-selection/syntax#specifying-resources) which will be added after the --select parameter.  
# MAGIC   Examples:  
# MAGIC     `dbt_gold_nyctaxi_trip` to run only the model with that name  
# MAGIC     `tag:nyctaxi_sql` to run everything with this tag.
# MAGIC     
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %pip install typing_extensions==4.8.0 dbt-semantic-interfaces==0.2.1 dbt-databricks==1.6.5 

# COMMAND ----------

# MAGIC %pip install --upgrade databricks-sdk

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

dbutils.widgets.dropdown("catalog", defaultValue="field_demos", choices=["field_demos", "hive_metastore"], label="Catalog")

dbutils.widgets.text("schema", defaultValue="dv_dev", label="Schema")

dbutils.widgets.text("selection_logic", defaultValue="")

# COMMAND ----------

import os
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
t = w.tokens.create(lifetime_seconds=300)
os.environ['DBT_DATABRICKS_TOKEN'] = t.token_value

# COMMAND ----------

# Setup environment variables for profile. Each person could have their own single node cluster with these set or could modify profiles.yml directly in their repos folder.
import os
os.environ['DBT_DATABRICKS_HOST'] = dbutils.secrets.get("db-field-eng", "dustin-secret2")
# os.environ['DBT_DATABRICKS_TOKEN'] = dbutils.secrets.get("db-field-eng", "dustin-secret")
os.environ['DBT_DATABRICKS_HTTP_PATH'] = dbutils.secrets.get("db-field-eng", "dustin-secret3")
os.environ['DBT_DATABRICKS_HTTP_PATH_CLUSTER'] = dbutils.secrets.get("db-field-eng", "dustin-secret4")

# TODO: Put the token or full profile in a volume that is restricted. Do you point dbt to that profile or copy locally to user directory. What is most secure for single user cluster? Can we make this short lived.

os.environ['DBT_DATABRICKS_SCHEMA'] = dbutils.widgets.get("schema")
os.environ['DBT_DATABRICKS_CATALOG'] = dbutils.widgets.get("catalog")

print(spark.conf.get("spark.databricks.clusterUsageTags.clusterId"))


# COMMAND ----------

selection_val = dbutils.widgets.get("selection_logic")
if selection_val != "":
  selection_logic = f"--select {selection_val}"
else:
  selection_logic = ""

os.environ["dbtselect"] = selection_logic

# COMMAND ----------

# MAGIC %sh sudo mkdir -p /local_disk0/tmp/.dbt ; echo $' 
# MAGIC dbt_databricks_examples:
# MAGIC   target: local
# MAGIC   outputs:
# MAGIC     #    #run DBT locally from your IDE and execute on a SQL warehouse (https://docs.getdbt.com/reference/warehouse-setups/databricks-setup)
# MAGIC     #    #Make sure you have pip install dbt-databricks in your local env
# MAGIC     #    #Run the project locally with:
# MAGIC     #    #DBT_DATABRICKS_HOST=xxx.cloud.databricks.com  DBT_DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxx DBT_DATABRICKS_TOKEN=dapixxxx dbt run
# MAGIC     local:
# MAGIC       type: databricks
# MAGIC       catalog: field_demos
# MAGIC       # schema: dv_dev2
# MAGIC       schema: "{{ env_var(\'DBT_DATABRICKS_SCHEMA\') }}"
# MAGIC       host: "{{ env_var(\'DBT_DATABRICKS_HOST\') }}"
# MAGIC       http_path: "{{ env_var(\'DBT_DATABRICKS_HTTP_PATH\') }}" #SQL warehouse Connection details
# MAGIC       token: '$DBT_DATABRICKS_TOKEN'
# MAGIC       threads: 3' > /local_disk0/tmp/.dbt/profiles.yml

# COMMAND ----------

# MAGIC %sh dbt run --profiles-dir /local_disk0/tmp/.dbt $dbtselect

# COMMAND ----------

# MAGIC %md
# MAGIC Alternative commands that could be useful. Feel free to remove.

# COMMAND ----------

# %sh dbt init --skip-profile-setup

# COMMAND ----------

# Alternative code
# import subprocess
# results = subprocess.run([f"dbt run {selection_logic}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# print(results)

