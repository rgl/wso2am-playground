# syntax=docker/dockerfile:1.4
FROM golang:1.20-bullseye as builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY *.go .
RUN CGO_ENABLED=0 go build -ldflags="-s"

# NB we use the bullseye-slim (instead of scratch) image so we can enter the container to execute bash etc.
FROM debian:bullseye-slim
RUN <<EOF
#!/bin/bash
set -euxo pipefail
apt-get update
apt-get install -y --no-install-recommends \
    wget \
    openssl \
    ca-certificates
rm -rf /var/lib/apt/lists/*
EOF
COPY --from=builder /app/example-go .
WORKDIR /
EXPOSE 8000
ENTRYPOINT ["/example-go"]