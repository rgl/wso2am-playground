# syntax=docker/dockerfile:1.4

FROM debian:bullseye-slim

RUN <<EOF
#!/bin/bash
set -euxo pipefail
apt-get update
apt-get install -y --no-install-recommends \
  python3 \
  python3-requests \
  unzip
rm -rf /var/lib/apt/lists/*
EOF

VOLUME /host

WORKDIR /host

ENTRYPOINT ["./init/init.sh"]
