#!/bin/bash
set -euxo pipefail

# initilize wso2am.
install -d tmp
python3 \
    init/init.py \
    wso2am-init \
    --base-url https://wso2am.test:9443
