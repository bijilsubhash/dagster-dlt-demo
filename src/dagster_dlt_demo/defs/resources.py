import dagster as dg
from dagster_dlt import DagsterDltResource
from dagster_gcp import GCSResource


@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "dlt_resource": DagsterDltResource(),
            "gcs": GCSResource()
        }
    )