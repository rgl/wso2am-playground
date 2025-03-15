#!/bin/bash
set -euxo pipefail

# update the trusted ca certificates.
# NB this is required to trust the wso2am ca.
# NB the wso2am ca is volume mounted inside the
#    /usr/local/share/ca-certificates directory.
update-ca-certificates

# initilize wso2am.
install -d tmp
python3 \
    init/init.py \
    wso2am-init \
    --base-url https://wso2am.test:9443
