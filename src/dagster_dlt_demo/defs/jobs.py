import dagster as dg

dummy_job = dg.define_asset_job(
    name="dummy_job",
    selection=dg.AssetSelection.groups("dlt-demo")
)