"""DynamoDB table construct for stock cache."""

from aws_cdk import RemovalPolicy
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType, BillingMode, TableClass
from constructs import Construct


class StockCacheTable(Construct):
    """
    DynamoDB table for caching stock analysis data.
    """

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        self.partition_key = "symbol"

        self.sort_key = "date"

        self.table = Table(
            self, "StockCacheTable",
            table_name="stock-cache",
            partition_key=Attribute(
                name=self.partition_key,
                type=AttributeType.STRING
            ),
            sort_key=Attribute(
                name=self.sort_key,
                type=AttributeType.STRING
            ),
            table_class=TableClass.STANDARD_INFREQUENT_ACCESS,
            billing_mode=BillingMode.PAY_PER_REQUEST,
            max_read_request_units=10,
            max_write_request_units=10,
            removal_policy=RemovalPolicy.DESTROY,
        )
