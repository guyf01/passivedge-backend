"""Synthetics canary: GET the health endpoint, fail the run on anything but 200."""

import os
import urllib.request


def handler(event, context):
    with urllib.request.urlopen(os.environ["HEALTH_URL"], timeout=20) as response:
        if response.status != 200:
            raise Exception(f"Health check returned {response.status}")
