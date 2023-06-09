# syntax=docker/dockerfile:1.4
# see https://github.com/wso2/product-apim
# see https://github.com/wso2/product-apim/releases/tag/v4.2.0
# see https://github.com/wso2/docker-is
# see https://apim.docs.wso2.com/en/latest/reference/working-with-the-source-code/

# see https://github.com/wso2/product-apim/releases
ARG WSO2AM_VERSION=4.2.0

# download the wso2am source code and build.
FROM maven:3.9.2-eclipse-temurin-11 as wso2am-build
ARG WSO2AM_VERSION
SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]
WORKDIR /build
RUN <<EOF
apt-get update
apt-get install -y --no-install-recommends \
    unzip
rm -rf /var/lib/apt/lists/*
EOF
RUN <<EOF
wget -qO wso2am.tgz https://github.com/wso2/product-apim/archive/refs/tags/v${WSO2AM_VERSION}.tar.gz
tar xf wso2am.tgz --strip-components=1
rm wso2am.tgz
EOF
RUN --mount=type=cache,target=/root/.m2 <<EOF
mvn clean install -Dmaven.test.skip=true
EOF
RUN <<EOF
set -euxo pipefail
unzip modules/distribution/product/target/wso2am-${WSO2AM_VERSION}.zip
mkdir /wso2am
mv wso2am-${WSO2AM_VERSION}/* /wso2am
rmdir wso2am-${WSO2AM_VERSION}
EOF

# create image.
FROM eclipse-temurin:11
WORKDIR /wso2am
EXPOSE 9443
RUN <<EOF
apt-get update
apt-get install -y --no-install-recommends \
    unzip \
    vim
rm -rf /var/lib/apt/lists/*
EOF
COPY --from=wso2am-build /wso2am ./
ENTRYPOINT ["./bin/api-manager.sh"]
