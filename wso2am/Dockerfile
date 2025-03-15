# syntax=docker.io/docker/dockerfile:1.14

# see https://hub.docker.com/r/wso2/wso2am
# see https://github.com/wso2/docker-apim
# see https://github.com/wso2/product-apim
# see https://github.com/wso2/product-apim/releases/tag/v4.3.0
ARG WSO2AM_VERSION=4.3.0

FROM wso2/wso2am:$WSO2AM_VERSION

# see https://apim.docs.wso2.com/en/4.3.0/install-and-setup/setup/deployment-best-practices/basic-health-checks/#api-m-runtime-health-checks
HEALTHCHECK \
    --start-period=5m \
    --start-interval=10s \
    --interval=30s \
    --timeout=10s \
    --retries=5 \
    CMD curl --no-progress-meter --fail --max-time 10 http://localhost:9763/api/am/gateway/v2/server-startup-healthcheck || exit 1
