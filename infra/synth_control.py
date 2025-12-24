#!/usr/bin/env python3
"""CDK App entry point."""
import sys

sys.path.append("..")
from infra.app import workload_app


def main():
    workload_app.create_stack()

    workload_app.synth()


if __name__ == "__main__":
    main()
