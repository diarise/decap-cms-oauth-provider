import os
import sys

import aws_cdk as cdk
from aws_cdk import Tags
from settings import settings

p = os.path.abspath("../decap_cms_oauth_provider")
sys.path.insert(1, p)
from stacks.lambda_api_stack import LambdaApiStack

from decap_cms_oauth_provider.settings import settings as lambda_env

app = cdk.App()
lambda_api_stack = LambdaApiStack(
    app,
    "DecapCMSOAuthProviderStack",
    env_name=settings.ENV,
    lambda_env=lambda_env,
    api_lambda_memory_size=settings.API_LAMBDA_MEMORY_SIZE,
    api_lambda_timeout=settings.API_LAMBDA_TIMEOUT,
    hosted_zone_name=settings.HOSTED_ZONE_NAME,
    hosted_zone_id=settings.HOSTED_ZONE_ID,
    domain_name=settings.DOMAIN_NAME,
    cert_arn=settings.CERTIFICATE_ARN,
    cors_allow_origin=settings.CORS_ALLOW_ORIGIN,
)


if settings.PROJECT:
    Tags.of(lambda_api_stack).add("project", settings.PROJECT)
if settings.PRODUCT:
    Tags.of(lambda_api_stack).add("product", settings.PRODUCT)
Tags.of(lambda_api_stack).add("env", settings.ENV)


app.synth()
