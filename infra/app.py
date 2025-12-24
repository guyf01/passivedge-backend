#!/usr/bin/env python3
"""CDK App entry point."""

import os
from aws_cdk import App, Stack, Environment


class WorkloadApp():
    """CDK App entry point."""

    def __init__(self):
        self.app = App()
    

    def create_stack(self):
        from infra.resources import StockCacheTable, StockAnalyzerFunction, StockAnalyzerApi, Route53Zone

        # Need explicit env for Route 53 hosted zone lookup
        self.stack = Stack(
            self.app, "PassivEdgeStack",
            env=Environment(
                account=os.environ.get('CDK_DEFAULT_ACCOUNT'),
                region=os.environ.get('CDK_DEFAULT_REGION'),
            )
        ) 

        self.stock_cache_table = StockCacheTable(self.stack, "StockCacheTable")

        self.stock_analysis_function = StockAnalyzerFunction(self.stack, "StockAnalyzerFunction")

        self.route53_zone = Route53Zone(self.stack, "Route53Zone")

        self.stock_analyzer_api = StockAnalyzerApi(self.stack, "StockAnalyzerApi")


    def synth(self):
        self.app.synth()


workload_app = WorkloadApp()
