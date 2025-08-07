import dagster as dg

from dagster_dlt_demo.defs.jobs import dummy_job
from dagster_dlt_demo.defs.sensor import sensors

defs = dg.Definitions(
    assets=dg.load_assets_from_package_name("dagster_dlt_demo.defs")
    jobs = [dummy_job],
    sensors=sensors
)

