# dbt databricks examples
---
This content contains unofficial examples of using dbt with Databricks. It can be used to test how Databricks can run dbt for SQL Models and Python Models, including running as tasks within a Databricks Workflow.

## Alternative dbt on Databricks demo

For more complete demos of dbt on Databricks, see the [dbdemos.ai](http://www.dbdemos.ai) c360 dbt bundle. To install and run that full demo with the worfklow and repo, you can run:
```
%pip install dbdemos
dbdemos.install('dbt-on-databricks')
```

## Running dbt on Databricks


## Running dbt + databricks locally
```
pip install dbt-databricks
export DBT_DATABRICKS_HOST=xxxx.cloud.databricks.com  
export DBT_DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxx
export  DBT_DATABRICKS_HTTP_PATH_CLUSTER=sql/protocolv1/o/11111xxx/0111-111111-11xxxxxx
export DBT_DATABRICKS_TOKEN=dapixxxxx
export DBT_DATABRICKS_SCHEMA=myschema
dbt run
```

### Project structure

This example repo has a few key directories. View each object/sub-folder mentioned below for more detail.
    
- ```dbt_project.yml```
    * Every dbt project requires a ```dbt_project.yml``` file - this is how dbt knows a directory is a dbt project
    * It contains information such as connection configurations to Databricks SQL Warehouses and where SQL transformation files are stored 

- ```profiles.yml```
    * This file stores profile configuration which dbt needs to connect to Databricks compute resources
    * Connection details such as the server hostname, HTTP path, catalog, db/schema information are configured here 
    
- ```models```
    * A model in dbt refers to a single ```.sql``` or ```.py``` file containing a modular data transformation block 
    * In this repo, we have modularized our transformations into bronze, silver, gold files in line with the Medallion Architecture 
    * Within each file, we can configure how the transformation will be materialized - either as a table, view, incremental, streaming_table, or materialized_view. Default will be table.

- ```tests```
    * Tests are assertions you make about your dbt models 
    * They are typically used for data quality and validation purposes
    * We also have the ability to quarantine and isolate records that fail a particular assertion

<br>