# Databricks notebook source
# MAGIC %md
# MAGIC ## Move new file into source path
# MAGIC When this section is enabled, it moves a new set of files to be processed.
# MAGIC Note: If the path is the same as production (or staging), this will impact production jobs also.

# COMMAND ----------

dbutils.widgets.text("base_path", "s3://<your_path>")

# COMMAND ----------

base_path = dbutils.widgets.get("base_path")

# COMMAND ----------

import re

files = dbutils.fs.ls(f"{base_path}/source/tripdata/yellow/")

loaded_months = []
for f in files:
  part_match = re.match("yellow_tripdata_(.*)\.csv\.gz" , f.name)
  loaded_months.append(part_match.group(1))

loaded_year, loaded_month = max(loaded_months).split('-')
if loaded_month == '12':
  year = loaded_year + 1
  month = '01'
else:
  year = loaded_year
  month = str(int(loaded_month) + 1).zfill(2)

print("Last loaded: ", loaded_year, loaded_month)
print("Next to load: ", year, month)


# COMMAND ----------

year_month = f"{year}-{month}"
dbutils.fs.cp(f"/databricks-datasets/nyctaxi/tripdata/yellow/yellow_tripdata_{year_month}.csv.gz", f"{base_path}/source/tripdata/yellow/yellow_tripdata_{year_month}.csv.gz")
