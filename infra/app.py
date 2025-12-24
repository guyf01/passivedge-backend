#!/usr/bin/env python3
"""CDK App entry point."""

from aws_cdk import App, Stack


class WorkloadApp():
    """CDK App entry point."""

    def __init__(self):
        self.app = App()
    

    def create_stack(self):
        from infra.resources import StockCacheTable

        self.stack = Stack(self.app, "PassivEdgeStack") 

        self.stock_cache_table = StockCacheTable(self.stack, "StockCacheTable")        


    def synth(self):
        self.app.synth()


workload_app = WorkloadApp()
