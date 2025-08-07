import dagster as dg

from dagster_dlt_demo.defs.jobs import dummy_job
from dagster_dlt_demo.defs.sensor import sensors
from dagster_dlt_demo.defs.SFTPIngestor.ingestor import orders_assets, customers_assets, products_assets

from dagster_dlt import DagsterDltResource
from dagster_gcp import GCSResource

defs = dg.Definitions(
    assets=[
        orders_assets, 
        customers_assets, 
        products_assets
        ],
    sensors=sensors,
    resources={
            "dlt_resource": DagsterDltResource(),
            "gcs": GCSResource()
        }
)

