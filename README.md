# About

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
* https://wso2am.test:9443/publisher/ (WSO2AM API Publisher; login as `admin`:`admin`)
* https://wso2am.test:9443/devportal/ (WSO2AM Developer Portal; login as `admin`:`admin`)
* https://wso2am.test:9443/carbon/ (WSO2AM Carbon Management Console; login as `admin`:`admin`)
* https://wso2am.test:8243/ (WSO2AM API Gateway)
* http://wso2am.test:8280/ (WSO2AM API Gateway)
* http://mail.test:8025 (MailHog (email server))

Try the example-go service:

* http://wso2am.test:8280/example-go/1.0.0/

Destroy everything:

```bash
./destroy.sh
```

# References

* https://apim.docs.wso2.com
  * https://apim.docs.wso2.com/en/latest/reference/understanding-the-new-configuration-model/
  * https://apim.docs.wso2.com/en/latest/reference/config-catalog/
* https://github.com/wso2/product-apim
