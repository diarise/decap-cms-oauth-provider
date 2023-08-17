# Decap CMS Oauth Provider CDK

After configuring environment variables following the template .env the application can be build and deployed using 

```
cdk deploy
```

### Architecture 

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


If HOSTED_ZONE_ID, HOSTED_ZONE_NAME, DOMAIN_NAME and CERTIFICATE_ARN variables are not set the HTTP API Gateway URL can be used and the resulting architecture will be very similar to the above but without Route53 handling DNS.

```
    ┌────────────────────┐            ┌──────────────┐
    │                    │            │              │
    │                    │            │              │
    │     AWS Lambda     │            │              │
    │     Python3.9      │            │   HTTP API   │
    │FastAPI/ASGI/Mangum │◀──────────▶│ API Gateway  │ 
    │                    │            │              │
    │                    │            │              │
    │                    │            │              │
    └────────────────────┘            └──────────────┘
```

