from pathlib import Path

from aws_cdk import CfnOutput, Duration, Stack, aws_lambda
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_cdk.aws_apigatewayv2 import ApiMapping, CorsHttpMethod, DomainName, HttpApi
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from aws_cdk.aws_certificatemanager import Certificate
from constructs import Construct
from stacks.utils import create_dependencies_layer, stringify_settings


class LambdaApiStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        env_name: str,
        lambda_env: dict,
        api_lambda_memory_size: int,
        api_lambda_timeout: int,
        cors_allow_origin: str,
        hosted_zone_name: str | None = None,
        hosted_zone_id: str | None = None,
        domain_name: str | None = None,
        cert_arn: str | None = None,
        **kwargs,
    ) -> None:
        """Lambda to handle api requests"""
        super().__init__(scope, id, **kwargs)

        api_lambda = aws_lambda.Function(
            self,
            f"decap-cms-oauth-provider-{env_name}-lambda",
            code=aws_lambda.Code.from_asset(
                path="../decap_cms_oauth_provider",
                exclude=[
                    "venv",
                    "__pycache__",
                    "pytest_cache",
                ],
            ),
            handler="decap_cms_oauth_provider.main.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            memory_size=api_lambda_memory_size,
            environment=stringify_settings(lambda_env),
            timeout=Duration.seconds(api_lambda_timeout),
            layers=[
                create_dependencies_layer(
                    self,
                    f"{env_name}",
                    "api",
                    Path("../decap_cms_oauth_provider/requirements.txt"),
                ),
            ],
        )

        api = HttpApi(
            self,
            f"{id}-endpoint",
            default_integration=HttpLambdaIntegration(
                f"decap-cms-oauth-provider-integration-{env_name}",
                api_lambda,
            ),
            cors_preflight={
                "allow_headers": [
                    "*",
                ],
                "allow_methods": [
                    CorsHttpMethod.GET,
                    CorsHttpMethod.POST,
                    CorsHttpMethod.HEAD,
                    CorsHttpMethod.OPTIONS,
                ],
                "allow_origins": [cors_allow_origin],
                "max_age": Duration.days(10),
            },
        )

        # When you dont include a default stage the api object does not include the url
        # However, the urls are all standard based on the api_id and the region
        api_url = f"https://{api.http_api_id}.execute-api.{self.region}.amazonaws.com"
        # TODO setup origin header to prevent traffic to API gateway directly
        CfnOutput(self, "Endpoint", value=api_url)

        if domain_name and cert_arn and hosted_zone_id and hosted_zone_name:
            custom_domain = DomainName(
                self,
                "customDomainName",
                domain_name=domain_name,
                certificate=Certificate.from_certificate_arn(
                    self, "custom_domain_cert", cert_arn
                ),
            )
            ApiMapping(
                self,
                "decap-cms-oauth-provider-api-mapping",
                api=api,
                domain_name=custom_domain,
            )
            hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
                self,
                f"decap-cms-oauth-provider-api-hosted-zone-{env_name}",
                hosted_zone_id=hosted_zone_id,
                zone_name=hosted_zone_name,
            )

            route53.ARecord(
                self,
                f"decap-cms-oauth-provider-api-alias-record-{env_name}",
                zone=hosted_zone,
                record_name=domain_name,
                target=route53.RecordTarget.from_alias(
                    targets.ApiGatewayv2DomainProperties(
                        custom_domain.regional_domain_name,
                        custom_domain.regional_hosted_zone_id,
                    )
                ),
            )
        else:
            print(
                f"""
            Could not add domain: {domain_name}
            cert: {cert_arn}
            zone_id: {hosted_zone_id}
            zone_name: {hosted_zone_name}
            """
            )
