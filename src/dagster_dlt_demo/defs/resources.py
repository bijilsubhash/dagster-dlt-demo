import dagster as dg
from dagster_dlt import DagsterDltResource
from dagster_duckdb import DuckDBResource
from dagster_gcp import GCSResource

dlt_resource = DagsterDltResource()
orders_duckdb = DuckDBResource(database="orders_to_duckdb.duckdb")
gcs_resource = GCSResource()

@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "dlt_resource": dlt_resource,
            "orders_duckdb": orders_duckdb,
            "gcs": gcs_resource
        }
    )