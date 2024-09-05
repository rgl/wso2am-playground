# syntax=docker.io/docker/dockerfile:1.9

# see https://github.com/wso2/product-apim-tooling/releases
# renovate: datasource=github-releases depName=wso2/product-apim-tooling
ARG WSO2AM_TOOLING_VERSION=4.3.1

FROM debian:bookworm-slim
ARG WSO2AM_TOOLING_VERSION

RUN <<EOF
#!/bin/bash
set -euxo pipefail
apt-get update
apt-get install -y --no-install-recommends \
  ca-certificates \
  python3 \
  python3-requests \
  unzip \
  wget
rm -rf /var/lib/apt/lists/*
EOF

RUN <<EOF
#!/bin/bash
set -euxo pipefail
url="https://github.com/wso2/product-apim-tooling/releases/download/v${WSO2AM_TOOLING_VERSION}/apictl-${WSO2AM_TOOLING_VERSION}-linux-amd64.tar.gz"
t="$(mktemp -q -d --suffix=.apictl)"
wget -qO- "$url" | tar xzf - -C "$t" --strip-components=1
install -m 755 "$t/apictl" /usr/local/bin/
rm -rf "$t"
EOF

VOLUME /host

WORKDIR /host

ENTRYPOINT ["./init/init.sh"]
