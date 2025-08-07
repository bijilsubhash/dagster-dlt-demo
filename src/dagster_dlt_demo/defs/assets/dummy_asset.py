import dagster as dg


@dg.asset(
    name="dummy_asset",
    description="A dummy asset",
)
def dummy_asset():
    return "Asset materialized successfully"