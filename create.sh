#!/bin/bash
set -euo pipefail

# destroy the existing environment.
docker compose down --remove-orphans --volumes

# build the environment.
docker compose build --progress plain

# start the environment in background.
docker compose up --detach

# wait for the services to exit.
function wait-for-service {
  echo "Waiting for the $1 service to complete..."
  while true; do
    result="$(docker compose ps --all --status exited --format json $1)"
    if [ -n "$result" ] && [ "$result" != 'null' ]; then
      exit_code="$(jq -r '.[].ExitCode' <<<"$result")"
      break
    fi
    sleep 3
  done
  docker compose logs $1
  return $exit_code
}
wait-for-service init

# show how to use the system.
cat <<'EOF'

#### Manual tests

example-go service:
  http://wso2am.test:8280/example-go/1.0.0/

wso2am:
  https://wso2am.test:9443/publisher/ (WSO2AM API Publisher; login as `admin`:`admin`)
  https://wso2am.test:9443/devportal/ (WSO2AM Developer Portal; login as `admin`:`admin`)
  https://wso2am.test:9443/carbon/ (WSO2AM Carbon Management Console; login as `admin`:`admin`)
EOF
