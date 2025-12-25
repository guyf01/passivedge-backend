"""API Gateway construct for stock analysis API."""

from aws_cdk import RemovalPolicy
from aws_cdk.aws_apigateway import RestApi, LambdaIntegration, EndpointConfiguration, EndpointType, DomainNameOptions, StageOptions, CorsOptions
from aws_cdk.aws_route53 import ARecord, RecordTarget
from aws_cdk.aws_route53_targets import ApiGatewayDomain
from constructs import Construct

from infra.app import workload_app


class StockAnalyzerApi(Construct):
    """
    REST API Gateway for stock analysis.
    """

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        self.api = RestApi(
            self, "StockAnalyzerApi",
            rest_api_name="PassivEdge Stock Analyzer",
            domain_name=DomainNameOptions(
                domain_name=workload_app.route53_zone.domain_name,
                certificate=workload_app.route53_zone.certificate,
            ),
            endpoint_configuration=EndpointConfiguration(
                types=[EndpointType.REGIONAL]
            ),
            cloud_watch_role_removal_policy=RemovalPolicy.DESTROY,
            disable_execute_api_endpoint=True,
            deploy_options=StageOptions(
                throttling_rate_limit=2,
                throttling_burst_limit=5,
            ),
            default_cors_preflight_options=CorsOptions(
                allow_origins=[f"https://{workload_app.route53_zone.domain_name}"],
                allow_methods=["POST", "OPTIONS"],
                allow_headers=["Content-Type"],
            ),
        )

        # Route 53 ALIAS record pointing to API Gateway
        ARecord(
            self, "AliasRecord",
            zone=workload_app.route53_zone.hosted_zone,
            target=RecordTarget.from_alias(ApiGatewayDomain(self.api.domain_name)),
        )

        # /analyze endpoint
        analyze = self.api.root.add_resource("analyze")
        analyze.add_method(
            "POST",
            LambdaIntegration(workload_app.stock_analysis_function.function, proxy=True),
        )
