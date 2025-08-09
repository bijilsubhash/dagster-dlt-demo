import dagster as dg

from dagster_dlt_demo.defs.sensor import sensors
from dagster_dlt_demo.defs.jobs import dummy_job
from dagster_dlt_demo.defs.SFTPIngestor.ingestor import orders_assets, customers_assets, products_assets

from dagster_dlt import DagsterDltResource
from dagster_gcp import GCSResource

defs = dg.Definitions(
    assets=[
        orders_assets, 
        customers_assets, 
        products_assets,
        dg.AssetSpec(key=dg.AssetKey("sftp_customers")),
        dg.AssetSpec(key=dg.AssetKey("sftp_orders")),
        dg.AssetSpec(key=dg.AssetKey("sftp_products"))
        ],
    sensors=sensors,
    jobs=[dummy_job],
    resources={
            "dlt_resource": DagsterDltResource(),
            "gcs": GCSResource()
        }
)

