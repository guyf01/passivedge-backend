"""Route 53 configuration for DNS."""

from aws_cdk.aws_route53 import HostedZone
from aws_cdk.aws_certificatemanager import Certificate, CertificateValidation
from constructs import Construct


class Route53Zone(Construct):
    """
    Route 53 hosted zone lookup and ALIAS record.
    """

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        self.domain_name = "passivedge.com"

        # Look up existing hosted zone
        self.hosted_zone = HostedZone.from_lookup(
            self, "HostedZone",
            domain_name=self.domain_name,
        )

        # Create ACM certificate with DNS validation
        self.certificate = Certificate(
            self, "Certificate",
            domain_name=self.domain_name,
            validation=CertificateValidation.from_dns(self.hosted_zone),
        )
