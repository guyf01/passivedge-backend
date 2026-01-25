"""Lambda function construct for stock analysis."""

from aws_cdk import Duration
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode
from constructs import Construct

from infra.app import workload_app


class StockAnalyzerFunction(Construct):
    """
    Lambda function for stock analysis (Docker-based).
    """

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        self.cors_origin = f"https://{workload_app.route53_zone.domain_name}"

        self.function = DockerImageFunction(
            self, "StockAnalyzerFunction",
            function_name="stock-analyzer",
            code=DockerImageCode.from_image_asset(directory="../stock-analyzer", asset_name="stock-analyzer", display_name="stock-analyzer"),
            memory_size=512,
            timeout=Duration.seconds(30),
            environment={
                "DYNAMODB_TABLE_NAME": workload_app.stock_cache_table.table.table_name,
                "DYNAMODB_PK": workload_app.stock_cache_table.partition_key,
                "DYNAMODB_SK": workload_app.stock_cache_table.sort_key,
                "CORS_ORIGIN": self.cors_origin,
            },
        )

        # Grant permissions
        workload_app.stock_cache_table.table.grant(self.function, "dynamodb:PutItem", "dynamodb:GetItem")
