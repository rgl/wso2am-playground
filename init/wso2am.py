from base64 import b64encode
import json
import logging
import requests
import time


def wait_for_ready(base_url):
    while True:
        try:
            r = requests.get(f'{base_url}/carbon/admin/login.jsp', verify=False)
            if r.status_code == 200:
                break
        except:
            time.sleep(3)


def dump_admin_settings(base_url):
    headers = {
        'Authorization': f'Basic {b64encode("admin:admin".encode("utf-8")).decode("ascii")}',
        'Content-Type': 'application/json',
    }
    resp = requests.get(
        url=f'{base_url}/api/am/admin/v4/settings',
        headers=headers,
        verify=False)
    resp.raise_for_status()
    response = resp.json()
    logging.debug("admin settings: %s", json.dumps(response, indent=2))
def init_main(args):
    # wait for wso2am to be available.
    wait_for_ready(args.base_url)


def try_main(args):
    dump_admin_settings(args.base_url)
