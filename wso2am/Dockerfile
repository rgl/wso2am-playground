# syntax=docker.io/docker/dockerfile:1.9

# see https://github.com/wso2/product-apim
# see https://github.com/wso2/product-apim/releases/tag/v4.2.0
# see https://github.com/wso2/docker-is
# see https://apim.docs.wso2.com/en/latest/reference/working-with-the-source-code/

# see https://github.com/wso2/product-apim/releases
ARG WSO2AM_VERSION=4.2.0

# download the wso2am source code and build.
FROM maven:3.9.8-eclipse-temurin-11 as wso2am-build
ARG WSO2AM_VERSION
SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]
WORKDIR /build
RUN <<EOF
#!/bin/bash
set -euxo pipefail
apt-get update
apt-get install -y --no-install-recommends \
    unzip
rm -rf /var/lib/apt/lists/*
EOF
RUN <<EOF
#!/bin/bash
set -euxo pipefail
wget -qO wso2am.tgz https://github.com/wso2/product-apim/archive/refs/tags/v${WSO2AM_VERSION}.tar.gz
tar xf wso2am.tgz --strip-components=1
rm wso2am.tgz
EOF
RUN --mount=type=cache,target=/root/.m2 <<EOF
#!/bin/bash
set -euxo pipefail
mvn clean install --batch-mode -Dmaven.test.skip=true
EOF
RUN <<EOF
#!/bin/bash
set -euxo pipefail
unzip modules/distribution/product/target/wso2am-${WSO2AM_VERSION}.zip
mkdir /wso2am
mv wso2am-${WSO2AM_VERSION}/* /wso2am
rmdir wso2am-${WSO2AM_VERSION}
EOF

# create image.
FROM eclipse-temurin:11
WORKDIR /wso2am
# API Publisher, Developer Portal, and Carbon Management Console.
EXPOSE 9443
# API Gateway (HTTPS and HTTP).
EXPOSE 8243 8280
# API Gateway (WSS and WS).
EXPOSE 8099 9099
RUN <<EOF
#!/bin/bash
set -euxo pipefail
apt-get update
apt-get install -y --no-install-recommends \
    unzip \
    vim
rm -rf /var/lib/apt/lists/*
EOF
COPY --from=wso2am-build /wso2am ./
# see https://apim.docs.wso2.com/en/4.2.0/install-and-setup/setup/deployment-best-practices/basic-health-checks/#api-m-runtime-health-checks
HEALTHCHECK \
    --start-period=5m \
    --start-interval=10s \
    --interval=30s \
    --timeout=10s \
    --retries=5 \
    CMD curl --no-progress-meter --fail --max-time 10 -u admin:admin http://localhost:9763/api/am/gateway/v2/server-startup-healthcheck || exit 1
ENTRYPOINT ["./bin/api-manager.sh"]
