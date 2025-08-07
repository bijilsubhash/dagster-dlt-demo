import dagster as dg

dummy_job = dg.define_asset_job(
    name="dummy_job",
    selection="dummy_asset",
)