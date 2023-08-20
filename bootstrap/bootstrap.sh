#!/bin/bash
set -euxo pipefail

ca_file_name='wso2am-ca'
ca_common_name='WSO2AM CA'
domain='wso2am.test'
store_password='abracadabra'

# create the CA data directory.
mkdir -p tmp/$ca_file_name
cd tmp/$ca_file_name

# create the CA certificate.
if [ ! -f $ca_file_name-crt.pem ]; then
    openssl genrsa \
        -out $ca_file_name-key.pem \
        2048 \
        2>/dev/null
    chmod 400 $ca_file_name-key.pem
    openssl req -new \
        -sha256 \
        -subj "/CN=$ca_common_name" \
        -key $ca_file_name-key.pem \
        -out $ca_file_name-csr.pem
    openssl x509 -req -sha256 \
        -signkey $ca_file_name-key.pem \
        -extensions a \
        -extfile <(echo "[a]
            basicConstraints=critical,CA:TRUE,pathlen:0
            keyUsage=critical,digitalSignature,keyCertSign,cRLSign
            ") \
        -days 365 \
        -in  $ca_file_name-csr.pem \
        -out $ca_file_name-crt.pem
    openssl x509 \
        -in $ca_file_name-crt.pem \
        -outform der \
        -out $ca_file_name-crt.der
    # dump the certificate contents (for logging purposes).
    #openssl x509 -noout -text -in $ca_file_name-crt.pem
fi

# trust the CA.
if [ ! -f /usr/local/share/ca-certificates/$ca_file_name.crt ]; then
    cp $ca_file_name-crt.pem /usr/local/share/ca-certificates/$ca_file_name.crt
    update-ca-certificates
fi

# create the server certificate.
# NB the localhost SAN is used by the wso2am applications (e.g. publisher).
if [ "$domain" != '' ] && [ ! -f $domain-crt.pem ]; then
    openssl genrsa \
        -out $domain-key.pem \
        2048 \
        2>/dev/null
    chmod 400 $domain-key.pem
    openssl req -new \
        -sha256 \
        -subj "/CN=$domain" \
        -key $domain-key.pem \
        -out $domain-csr.pem
    openssl x509 -req -sha256 \
        -CA $ca_file_name-crt.pem \
        -CAkey $ca_file_name-key.pem \
        -CAcreateserial \
        -extensions a \
        -extfile <(echo "[a]
            subjectAltName=DNS:$domain,DNS:localhost
            extendedKeyUsage=critical,serverAuth
            ") \
        -days 365 \
        -in  $domain-csr.pem \
        -out $domain-crt.pem
    openssl pkcs12 -export \
        -keyex \
        -inkey $domain-key.pem \
        -in $domain-crt.pem \
        -certfile $domain-crt.pem \
        -passout pass: \
        -out $domain-key.p12
    # dump the certificate contents (for logging purposes).
    #openssl x509 -noout -text -in $domain-crt.pem
    #openssl pkcs12 -info -nodes -passin pass: -in $domain-key.p12
fi

# create the wso2am truststore.
if [ ! -f wso2am-truststore.p12 ]; then
    keytool \
        -import \
        -noprompt \
        -file $ca_file_name-crt.pem \
        -alias wso2am \
        -storetype PKCS12 \
        -storepass "$store_password" \
        -keystore wso2am-truststore.p12
    keytool \
        -v \
        -list \
        -storetype PKCS12 \
        -storepass "$store_password" \
        -keystore wso2am-truststore.p12
fi

# create the wso2am keystore.
if [ ! -f wso2am-keystore.p12 ]; then
    keytool \
        -v \
        -importkeystore \
        -srcstoretype PKCS12 \
        -srckeystore $domain-key.p12 \
        -srcstorepass '' \
        -srcalias 1 \
        -deststoretype PKCS12 \
        -destkeystore wso2am-keystore.p12 \
        -deststorepass "$store_password" \
        -destalias wso2am
    keytool \
        -v \
        -list \
        -storetype PKCS12 \
        -storepass "$store_password" \
        -keystore wso2am-keystore.p12
fi

# try the truststore and keystore from a java application.
javac -d /tmp ../../bootstrap/List.java
java -cp /tmp List
