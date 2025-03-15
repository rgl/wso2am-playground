import java.io.FileInputStream;
import java.security.KeyStore;
import java.security.KeyStore.Entry;
import java.security.KeyStore.ProtectionParameter;
import java.security.cert.Certificate;
import java.security.cert.X509Certificate;
import java.util.Collections;

public class List {
    public static void main(String[] args) throws Exception {
        char[] password = "opensesame".toCharArray();
        dumpKeyStore("wso2am-truststore.p12", password, null);
        dumpKeyStore("wso2am-keystore.p12", password, password);
    }

    private static void dumpKeyStore(String fileName, char[] keystorePassword, char[] entriesPassword) throws Exception {
        ProtectionParameter entriesPasswordParameter = null;
        if (entriesPassword != null) {
            entriesPasswordParameter = new KeyStore.PasswordProtection(entriesPassword);
        }
        KeyStore keyStore = KeyStore.getInstance("PKCS12");
        FileInputStream fis = new FileInputStream(fileName);
        keyStore.load(fis, keystorePassword);
        for (String alias : Collections.list(keyStore.aliases())) {
            Entry entry = keyStore.getEntry(alias, entriesPasswordParameter);
            if (entry instanceof KeyStore.PrivateKeyEntry) {
                System.out.println(fileName + " Alias " + alias + " Type: Private Key Entry");
            } else if (entry instanceof KeyStore.TrustedCertificateEntry) {
                System.out.println(fileName + " Alias " + alias + " Type: Trusted Certificate Entry");
            } else {
                System.out.println(fileName + " Alias " + alias + " Type: Unknown");
            }
            Certificate certificate = keyStore.getCertificate(alias);
            if (certificate instanceof X509Certificate) {
                X509Certificate crt = (X509Certificate) certificate;
                System.out.println(fileName + " Alias " + alias + " Certificate Subject: " + crt.getSubjectX500Principal());
                System.out.println(fileName + " Alias " + alias + " Certificate Issuer: " + crt.getIssuerX500Principal());
            }
        }
    }
}
