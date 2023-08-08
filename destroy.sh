#!/bin/bash
set -euo pipefail

# destroy the existing environment.
docker compose kill --remove-orphans
docker compose down --remove-orphans --volumes
