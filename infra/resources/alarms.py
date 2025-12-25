"""CloudWatch alarms for monitoring."""

from aws_cdk import Duration
from aws_cdk.aws_cloudwatch import ComparisonOperator, TreatMissingData, Alarm
from constructs import Construct

from infra.app import workload_app


class ApiGatewayAlarms(Construct):
    """CloudWatch alarms for API Gateway monitoring."""

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        self.server_error_alarm = Alarm(
            self, "ServerErrorAlarm",
            alarm_name="stock-analyzer-5xx-errors",
            metric=workload_app.stock_analyzer_api.api.metric_server_error(
                period=Duration.minutes(1),
            ),
            threshold=1,
            evaluation_periods=1,
            comparison_operator=ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treat_missing_data=TreatMissingData.NOT_BREACHING,
        )

        self.client_error_alarm = Alarm(
            self, "ClientErrorAlarm",
            alarm_name="stock-analyzer-4xx-errors",
            metric=workload_app.stock_analyzer_api.api.metric_client_error(
                period=Duration.minutes(1),
            ),
            threshold=1,
            evaluation_periods=1,
            comparison_operator=ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treat_missing_data=TreatMissingData.NOT_BREACHING,
        )

        self.high_traffic_alarm = Alarm(
            self, "HighTrafficAlarm",
            alarm_name="stock-analyzer-high-traffic",
            metric=workload_app.stock_analyzer_api.api.metric_count(
                period=Duration.minutes(1),
            ),
            threshold=100,
            evaluation_periods=1,
            comparison_operator=ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treat_missing_data=TreatMissingData.NOT_BREACHING,
        )
