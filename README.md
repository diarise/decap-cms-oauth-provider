# Decap CMS OAuth Provider

A Python3.9 GitHub OAuth Provider for Decap CMS that can run on AWS Lambda. 

Adapted from https://github.com/davidejones/netlify-cms-oauth-provider-python.git

## Development

At the project root create an environment file named `.env` with the following environment variables:


```env
PROJECT=project
PRODUCT=website
ENV=prod
OAUTH_CLIENT_ID=123456789abcdefg
OAUTH_CLIENT_SECRET=mysupersecretkeymysupersecretkeymysupersecretkey
HOSTED_ZONE_ID=ABCDEFGHIJKLMN
HOSTED_ZONE_NAME=example.com
DOMAIN_NAME=demo.example.com
CERTIFICATE_ARN=arn:aws:acm:us-east-1:9999999999:certificate/a123456789-1234-567f-89f0-1234a5cde67f
API_LAMBDA_MEMORY_SIZE=128
API_LAMBDA_TIMEOUT=10
```

Variables:

* PROJECT - string value for AWS `project` tag. Optional.
* PRODUCT - string value for AWS `product` tag. Optional.
* ENV - string value for AWS`env` tag and CDK/Cloudformation naming. Optional, defaults to 'staging'
* OAUTH_CLIENT_ID - Github OAuth Client ID https://github.com/settings/applications/new
* OAUTH_CLIENT_SECRET - Github OAuth Client Secret https://github.com/settings/applications/new
* HOSTED_ZONE_ID - Route53 hosted zone ID of the custom domain name. Optional if not set API gateway url can be used, if set must be set with HOSTED_ZONE_NAME, DOMAIN_NAME and CERTIFICATE_ARN
* HOSTED_ZONE_NAME - Route53 hosted zone name of the custom domain name. Optional if not set API gateway url can be used, if set must be set with HOSTED_ZONE_ID, DOMAIN_NAME and CERTIFICATE_ARN
* DOMAIN_NAME - domain name for the service. Optional if not set API gateway url can be used, if set must be set with HOSTED_ZONE_ID, HOSTED_ZONE_NAME and CERTIFICATE_ARN
* CERTIFICATE_ARN - AWS ARN (Amazon Resource Name) for TLS certificate for the custom domain name. Optional if not set API gateway url can be used, if set must be set with HOSTED_ZONE_ID, HOSTED_ZONE_NAME and DOMAIN_NAME
* API_LAMBDA_MEMORY_SIZE - number of MB(Megabytes) to allocate to AWS Lambda. Optional, defaults to 128
* API_LAMBDA_TIMEOUT - number of seconds before timeout for AWS Lambda. Optional, defaults to 10

### Infrastructure

 This implementation is designed to run on AWS Lambda functions. Infrastructure is defined using AWS CDK (Cloud development kit) and is available in the `cdk` directory of the repository. 


#### Overview

 The FastAPI application runs on a lambda function with help from the [mangum](https://github.com/jordaneremieff/mangum) package to wrap `asgi` for use on Lambda. The Lambda function is proxied using AWS HTTP Api Gateway. An optional custom domain name can be configured to point to the API Gateway URL using AWS Route53. 

```
    ┌────────────────────┐            ┌──────────────┐              ┌──────────────┐
    │                    │            │              │              │              │
    │                    │            │              │              │              │
    │     AWS Lambda     │            │              │              │              │
    │     Python3.9      │            │   HTTP API   │              │ Route53 DNS  │
    │FastAPI/ASGI/Mangum │◀──────────▶│ API Gateway  │ ◀───────────▶│   ARecord    │
    │                    │            │              │              │              │
    │                    │            │              │              │              │
    │                    │            │              │              │              │
    └────────────────────┘            └──────────────┘              └──────────────┘
```


#### Deployment

 To deploy the application set the required environment variables either through an `.env` as described above or through your environment of choice. Read more about CDK in the `cdk` directory `README.md`.

 To deploy run:

 ```sh
cdk deploy
 ```