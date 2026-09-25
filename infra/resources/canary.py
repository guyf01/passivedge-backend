"""Synthetic canary health check for the stock analyzer API."""

from aws_cdk import Duration
from aws_cdk.aws_s3 import LifecycleRule
from aws_cdk.aws_synthetics import Canary, Code, Runtime, Schedule, Test
from constructs import Construct

from infra.app import workload_app


class HealthCheckCanary(Construct):
    """
    Weekly end-to-end request through Route 53, ACM, API Gateway and Lambda.
    Also keeps the container-image Lambda from going Inactive when idle for weeks.
    """

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        api = workload_app.stock_analyzer_api

        self.canary = Canary(
            self, "HealthCheckCanary",
            canary_name="stock-analyzer-health",
            schedule=Schedule.cron(week_day="MON", hour="12", minute="0"),
            runtime=Runtime.SYNTHETICS_PYTHON_SELENIUM_7_0,
            test=Test.custom(
                code=Code.from_asset("../health-check-canary"),
                handler="health_check.handler",
            ),
            environment_variables={
                "HEALTH_URL": f"https://{api.api_domain_name}{api.analyze_health_resource.path}",
            },
            artifacts_bucket_lifecycle_rules=[LifecycleRule(expiration=Duration.days(30))],
            timeout=Duration.seconds(60),
            provisioned_resource_cleanup=True,
        )
