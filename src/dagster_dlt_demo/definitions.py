import dagster as dg

from dagster_dlt_demo.defs.jobs import dummy_job
from dagster_dlt_demo.defs.sensor import sensors
from dagster_dlt_demo.defs.SFTPIngestor.ingestor import orders_assets, customers_assets, products_assets

defs = dg.Definitions(
    assets=[
        dg.load_assets_from_package_name("dagster_dlt_demo.defs"), 
        orders_assets, 
        customers_assets, 
        products_assets
        ],
    jobs = [dummy_job],
    sensors=sensors
)

