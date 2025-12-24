"""Lambda function construct for stock analysis."""

from aws_cdk import Duration
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode
from constructs import Construct

from infra.app import workload_app


class StockAnalysisFunction(Construct):
    """
    Lambda function for stock analysis (Docker-based).
    """

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        self.function = DockerImageFunction(
            self, "StockAnalysisFunction",
            function_name="stock-analysis",
            code=DockerImageCode.from_image_asset(directory="..", asset_name="stock-analysis"),
            memory_size=512,
            timeout=Duration.seconds(30),
            environment={
                "DYNAMODB_TABLE_NAME": workload_app.stock_cache_table.table.table_name,
            },
        )

        # Grant permissions
        workload_app.stock_cache_table.table.grant(self.function, "dynamodb:PutItem", "dynamodb:GetItem")
