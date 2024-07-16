#!/bin/bash
set -euo pipefail

# destroy the existing environment.
./destroy.sh

# build the environment.
docker compose --progress plain build

# start the environment in background.
docker compose up --detach

# wait for the services to exit.
function wait-for-service {
  echo "Waiting for the $1 service to complete..."
  while true; do
    local result="$(docker compose ps --status exited --format json $1)"
    if [ -n "$result" ] && [ "$result" != 'null' ]; then
      local exit_code="$(jq -r '.ExitCode' <<<"$result")"
      break
    fi
    sleep 3
  done
  docker compose logs $1
  return $exit_code
}
wait-for-service init

# wait for the example-go service to be available.
function wait-for-http-200 {
  local url="$1"
  local timeout=300 # NB 300s is 5m.
  local start_time="$(date +%s)"

  echo "Waiting for the $url URL to be available..."

  while true; do
    local status_code="$(curl -o /dev/null -s -w "%{http_code}" "$url")"
    local current_time="$(date +%s)"
    local elapsed_time="$((current_time - start_time))"

    if [ "$status_code" -eq 200 ]; then
      echo "URL is available after $elapsed_time seconds."
      return 0
    fi

    if [ "$elapsed_time" -ge "$timeout" ]; then
      echo "Timeout reached. URL did not return 200 status code within $timeout seconds."
      return 1
    fi

    sleep 5
  done
}
wait-for-http-200 http://wso2am.test:8280/example-go/1.0.0/

# show how to use the system.
cat <<'EOF'

#### Manual tests

example-go service:
  http://example-go.test:8000
  http://wso2am.test:8280/example-go/1.0.0/
  https://wso2am.test:8243/example-go/1.0.0/

wso2am:
  http://wso2am.test:8280/ (WSO2AM Gateway)
  https://wso2am.test:8243/ (WSO2AM Gateway)
  https://wso2am.test:9443/carbon/ (WSO2AM Carbon Management Console; login as `admin`:`admin`)
  https://wso2am.test:9443/admin/ (WSO2AM Admin Portal; login as `admin`:`admin`)
  https://wso2am.test:9443/publisher/ (WSO2AM Publisher; login as `admin`:`admin`)
  https://wso2am.test:9443/devportal/ (WSO2AM Developer Portal; login as `admin`:`admin`)
EOF
