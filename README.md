# About

[![Build](https://github.com/rgl/wso2am-playground/actions/workflows/build.yml/badge.svg)](https://github.com/rgl/wso2am-playground/actions/workflows/build.yml)

This is a [WSO2AM (WSO2 API Manager)](https://wso2.com/api-manager/) playground.

# Usage

Install docker compose.

Add the following entries to your machine `hosts` file:

```
127.0.0.1 wso2am.test
127.0.0.1 mail.test
127.0.0.1 example-go.test
```

Start the environment:

```bash
./create.sh
```

When anything goes wrong, you can try to troubleshoot at:

* `docker compose logs --follow`
* https://wso2am.test:9443/admin/ (WSO2AM Admin Portal; login as `admin`:`admin`)
* https://wso2am.test:9443/publisher/ (WSO2AM Publisher; login as `admin`:`admin`)
* https://wso2am.test:9443/devportal/ (WSO2AM Developer Portal; login as `admin`:`admin`)
* https://wso2am.test:9443/carbon/ (WSO2AM Carbon Management Console; login as `admin`:`admin`)
* https://wso2am.test:8243/ (WSO2AM Gateway)
* http://wso2am.test:8280/ (WSO2AM Gateway)
* http://mail.test:8025 (Email Server)

Try the example-go service:

* http://wso2am.test:8280/example-go/1.0.0/

Destroy everything:

```bash
./destroy.sh
```

List this repository dependencies (and which have newer versions):

```bash
GITHUB_COM_TOKEN='YOUR_GITHUB_PERSONAL_TOKEN' ./renovate.sh
```

# References

* https://apim.docs.wso2.com
  * https://apim.docs.wso2.com/en/latest/reference/understanding-the-new-configuration-model/
  * https://apim.docs.wso2.com/en/latest/reference/config-catalog/
  * https://apim.docs.wso2.com/en/latest/reference/product-apis/overview/
* https://github.com/wso2/product-apim
* https://github.com/wso2/api-manager/issues
