import io

import dlt
from dlt.extract.resource import DltResource
import polars as pl
import dagster as dg

from collections.abc import Iterable

from dlt import pipeline
from dlt.sources.filesystem import filesystem
from dlt.common.configuration.specs import SFTPCredentials

from dagster import AssetExecutionContext

from dagster_dlt_demo.common.utils.logging_util import Logger
from dagster_dlt import DagsterDltResource, DagsterDltTranslator, dlt_assets



logger = Logger(__name__)

external_asset_keys = {
    "customers": dg.SourceAsset(key="sftp_customers"),
    "orders": dg.SourceAsset(key="sftp_orders"),
    "products": dg.SourceAsset(key="sftp_products")
}

class CustomDagsterDltTranslator(DagsterDltTranslator):
    def get_asset_spec(self, data) -> dg.AssetSpec:
        """Overrides asset spec to override upstream asset key to be a single source asset."""
        default_spec = super().get_asset_spec(data)
        return default_spec.replace_attributes(
            key=dg.AssetKey(f"dlt_{data.resource.name}"),
            deps=[external_asset_keys[data.resource.name]]
        )
    
def create_sftp_source(resource_name: str, file_glob: str):
    @dlt.source(name=f"{resource_name}_source")
    def sftp_source():
        @dlt.resource(name=resource_name)
        def resource():
            file = filesystem(
                bucket_url="sftp://eu-central-1.sftpcloud.io/input/20250805",
                credentials=SFTPCredentials(
                sftp_username=dg.EnvVar("userName").get_value(),
                sftp_password=dg.EnvVar("password").get_value(),
                sftp_port=dg.EnvVar("port").get_value(),
                sftp_look_for_keys=False,
                sftp_allow_agent=False,
            ),
                file_glob=file_glob
            )

            for item in file:
                with item.open() as f:
                    f.seek(0)
                    file_data = f.read().decode('utf-8')
                    logger.info(f"File data length: {len(file_data)}")
                    
                    if not file_data.strip():
                        logger.info("File is empty")
                        continue
                        
                    df = pl.read_csv(io.StringIO(file_data))
                    yield from df.to_dicts()
        
        return resource
    
    return sftp_source

def create_dlt_assets(resource_name: str, file_glob: str):
    source = create_sftp_source(resource_name, file_glob)
    
    @dlt_assets(
        dlt_source=source(),
        dlt_pipeline=pipeline(
            pipeline_name=f"{resource_name}_to_duckdb",
            dataset_name=f"{resource_name}",
            destination='filesystem',
            progress="log"
        ),
        name=f"{resource_name}_assets",
        dagster_dlt_translator=CustomDagsterDltTranslator(),
        group_name="dltdemo"
    )
    def assets(context: AssetExecutionContext, dlt_resource: DagsterDltResource):
        dlt.config['destination.filesystem.layout'] = "{table_name}/{YYYY}{MM}{DD}/{mm}/{load_id}.{file_id}.{ext}"
        dlt.secrets['destination.filesystem.bucket_url'] = dg.EnvVar('DESTINATION__FILESYSTEM__CREDENITIALS__PROJECT_ID')
        dlt.secrets['destination.filesystem.credentials.bucket_url'] = dg.EnvVar('DESTINATION__BUCKET_URL')
        dlt.secrets['destination.filesystem.credentials.private_key'] = dg.EnvVar('DESTINATION__FILESYSTEM__CREDENITIALS__PRIVATE_KEY')
        dlt.secrets['destination.filesystem.credentials.client_email'] = dg.EnvVar('DESTINATION__FILESYSTEM__CREDENITIALS__CLIENT_EMAIL')
        yield from dlt_resource.run(context=context)
    
    return assets

# Create assets for each resource
orders_assets = create_dlt_assets("orders", "orders.csv")
customers_assets = create_dlt_assets("customers", "customers.csv")
products_assets = create_dlt_assets("products", "products.csv")

# @dg.asset_check(asset=dg.AssetKey("orders"))
# def data_quality_check() -> dg.AssetCheckResult:
#     with orders_duckdb.get_connection() as conn:
#         result = conn.execute("""
#             SELECT COUNT(*) as null_count
#             FROM orders_data.orders
#             WHERE order_id IS NULL
#         """).fetchone()

#         null_count = result[0] if result else 0

#         return dg.AssetCheckResult(
#             passed=null_count == 1,
#             metadata={"null_values_found": null_count}
#         )
