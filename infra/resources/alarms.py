"""CloudWatch alarms for monitoring with email notifications."""

from aws_cdk import Duration
from aws_cdk.aws_cloudwatch import ComparisonOperator, TreatMissingData, Alarm
from aws_cdk.aws_cloudwatch_actions import SnsAction
from aws_cdk.aws_logs import MetricFilter, FilterPattern
from aws_cdk.aws_sns import Topic
from aws_cdk.aws_sns_subscriptions import EmailSubscription
from constructs import Construct

from infra.app import workload_app


class ApiGatewayAlarms(Construct):
    """CloudWatch alarms for API Gateway monitoring."""

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Get email from CDK context
        alert_email = self.node.try_get_context("alert-email")
        if not alert_email:
            raise ValueError(
                "Missing 'alert-email' context. "
                "Add to cdk.context.json: {\"alert-email\": \"your@email.com\"}"
            )

        alarm_topic = Topic(
            self, "AlarmTopic",
            topic_name="stock-analyzer-alarms",
        )

        alarm_topic.add_subscription(EmailSubscription(alert_email))

        alarm_action = SnsAction(alarm_topic)

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
        self.server_error_alarm.add_alarm_action(alarm_action)

        user_error_filter = MetricFilter(
            self, "UserErrorFilter",
            log_group=workload_app.stock_analyzer_api.access_log_group,
            filter_pattern=FilterPattern.all(
                FilterPattern.string_value("$.resourcePath", "=", workload_app.stock_analyzer_api.analyze_resource.path),
                FilterPattern.number_value("$.status", ">=", 400),
                FilterPattern.number_value("$.status", "<", 500),
            ),
            metric_namespace="PassivEdge/ApiGateway",
            metric_name="UserErrors",
            default_value=0,
        )

        self.user_error_alarm = Alarm(
            self, "UserErrorAlarm",
            alarm_name="stock-analyzer-user-errors",
            metric=user_error_filter.metric(
                period=Duration.minutes(1),
                statistic="Sum",
            ),
            threshold=5,
            evaluation_periods=1,
            comparison_operator=ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treat_missing_data=TreatMissingData.NOT_BREACHING,
        )
        self.user_error_alarm.add_alarm_action(alarm_action)

        security_probe_filter = MetricFilter(
            self, "SecurityProbeFilter",
            log_group=workload_app.stock_analyzer_api.access_log_group,
            filter_pattern=FilterPattern.string_value("$.resourcePath", "!=", workload_app.stock_analyzer_api.analyze_resource.path),
            metric_namespace="PassivEdge/ApiGateway",
            metric_name="SecurityProbes",
            default_value=0,
        )

        self.security_probe_alarm = Alarm(
            self, "SecurityProbeAlarm",
            alarm_name="stock-analyzer-security-probes",
            metric=security_probe_filter.metric(
                period=Duration.minutes(1),
                statistic="Sum",
            ),
            threshold=20,
            evaluation_periods=1,
            comparison_operator=ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treat_missing_data=TreatMissingData.NOT_BREACHING,
        )
        self.security_probe_alarm.add_alarm_action(alarm_action)

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
        self.high_traffic_alarm.add_alarm_action(alarm_action)
