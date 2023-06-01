from base64 import b64encode
from urllib.parse import urlparse, urljoin
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


def find_api(base_url, name):
    # see https://apim.docs.wso2.com/en/latest/reference/product-apis/publisher-apis/publisher-v4/publisher-v4/#tag/APIs
    headers = {
        'Authorization': f'Basic {b64encode("admin:admin".encode("utf-8")).decode("ascii")}',
        'Content-Type': 'application/json',
    }
    resp = requests.get(
        url=f'{base_url}/api/am/publisher/v4/apis',
        params={
            'query': f'name:{name}',
        },
        headers=headers,
        verify=False)
    resp.raise_for_status()
    response = resp.json()
    if response['count'] == 0:
        return None
    return response['list'][0]


def dump_api(base_url, name):
    api = find_api(base_url, name)
    if not api:
        return
    logging.debug("api %s response: %s",
        name,
        json.dumps(api, indent=2))


def create_api(base_url, config):
    name = config['name']
    headers = {
        'Authorization': f'Basic {b64encode("admin:admin".encode("utf-8")).decode("ascii")}',
        'Content-Type': 'application/json',
    }
    apis_url = f'{base_url}/api/am/publisher/v4/apis'

    # create the api.
    # NB when the api already exists, it will not be updated/deployed/published.
    api = find_api(base_url, name)
    if api:
        id = api['id']
        logging.debug('skipping the api %s creation as it already exists with id %s', name, id)
    else:
        # create the api.
        # see https://apim.docs.wso2.com/en/latest/reference/product-apis/publisher-apis/publisher-v4/publisher-v4/#tag/APIs/operation/createAPI
        # NB this returns an HTTP 201 Created with a location header that has the
        #    api id.
        #    e.g. Location: https://wso2am.test:9443/api/am/publisher/apis/60850f16-7f35-449f-960a-d9f4e4ad4208
        logging.debug('creating the api %s', name)
        resp = requests.post(
            url=apis_url,
            headers=headers,
            json=config,
            verify=False)
        resp.raise_for_status()
        location = urlparse(resp.headers['Location'])
        id = location.path.split('/')[-1]
        logging.debug('created the api %s with id %s', name, id)

        # create an api revision.
        # see https://apim.docs.wso2.com/en/latest/reference/product-apis/publisher-apis/publisher-v4/publisher-v4/#tag/API-Revisions/operation/createAPIRevision
        logging.debug('creating an api %s revision', name)
        resp = requests.post(
            url=f'{apis_url}/{id}/revisions',
            headers=headers,
            json={
            },
            verify=False)
        resp.raise_for_status()
        location = urlparse(resp.headers['Location'])
        revision_id = location.path.split('/')[-1]
        logging.debug('created the api %s revision with id %s', name, revision_id)

        # deploy the api revision.
        # see https://apim.docs.wso2.com/en/latest/reference/product-apis/publisher-apis/publisher-v4/publisher-v4/#tag/API-Revisions/operation/deployAPIRevision
        logging.debug('deploying the api %s revision with id %s', name, revision_id)
        resp = requests.post(
            url=f'{apis_url}/{id}/deploy-revision',
            headers=headers,
            params={
                'revisionId': revision_id,
            },
            json=[
                {
                    "vhost": "localhost",
                    "name": "Default",
                    "displayOnDevportal": True,
                }
            ],
            verify=False)
        resp.raise_for_status()

        # publish the api.
        # see https://apim.docs.wso2.com/en/latest/reference/product-apis/publisher-apis/publisher-v4/publisher-v4/#tag/API-Lifecycle/operation/changeAPILifecycle
        logging.debug('publishing the api %s', name)
        resp = requests.post(
            url=f'{apis_url}/change-lifecycle',
            headers=headers,
            params={
                'action': 'Publish',
                'apiId': id,
            },
            verify=False)
        resp.raise_for_status()

    # return the api details.
    # see https://apim.docs.wso2.com/en/latest/reference/product-apis/publisher-apis/publisher-v4/publisher-v4/#tag/APIs/operation/getAPI
    resp = requests.get(
        url=f'{apis_url}/{id}',
        headers=headers,
        verify=False)
    resp.raise_for_status()
    return resp.json()


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


def create_example_go_api(base_url):
    create_api(
        base_url,
        {
            "name": "example-go",
            "context": "/example-go",
            "version": "1.0.0",
            "type": "HTTP",
            "policies": [
                "Unlimited",
            ],
            "endpointConfig": {
                "endpoint_type": "http",
                "production_endpoints": {
                    "url": "http://example-go.test:8000"
                }
            },
            "operations": [
                {
                    "target": "/*",
                    "verb": "GET",
                    "authType": "None",
                    "throttlingPolicy": "Unlimited"
                },
            ]
        })


def init_main(args):
    # wait for wso2am to be available.
    wait_for_ready(args.base_url)

    # create apis.
    create_example_go_api(args.base_url)

def try_main(args):
    dump_admin_settings(args.base_url)
    dump_api(args.base_url, 'example-go')
