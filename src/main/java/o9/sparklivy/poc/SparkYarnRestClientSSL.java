package o9.sparklivy.poc;

import java.io.IOException;
import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.List;
import java.security.KeyStore;
import javax.net.ssl.SSLContext;

import lombok.extern.slf4j.Slf4j;

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.security.kerberos.client.KerberosRestTemplate;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.security.UserGroupInformation;

import org.apache.http.conn.ssl.SSLContexts;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.client.HttpClient;
import org.apache.http.impl.client.HttpClients;

@Slf4j
public class SparkYarnRestClientSSL {

    public static void main(String[] arguments) {

        // keberos
        Configuration conf = new Configuration();
        conf.set("hadoop.security.authentication", "Kerberos");

        UserGroupInformation.setConfiguration(conf);

        System.setProperty("java.security.auth.login.config", "true");

        String kerberosUser = "yang.wang@AMER.O9SOLUTIONS.LOCAL";
        String keytabLocation = "/home/liveadmin/yangwang2.keytab";

        try {
            UserGroupInformation.loginUserFromKeytab(kerberosUser, keytabLocation);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        System.out.println("Auth Completed");

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);


        HttpClient httpClient = null;
        String keystoreFile = "/home/liveadmin/livytruststore.jks";
        String password = "password1";

        FileInputStream inputStream = null;
        try {
            inputStream = new FileInputStream(keystoreFile);
            KeyStore trustStore = KeyStore.getInstance(KeyStore.getDefaultType());
            trustStore.load(new FileInputStream(keystoreFile), password.toCharArray());
            SSLContext sslContext = SSLContexts.custom()
                    .loadTrustMaterial(trustStore)
                    .build();
            SSLConnectionSocketFactory csf = new SSLConnectionSocketFactory(sslContext);
            httpClient = HttpClients.custom().setSSLSocketFactory(csf).build();
        } catch (Exception e) {
            throw new RuntimeException("Failed to create SSL HttpClient", e);
        } finally {
            if (inputStream != null) {
                try {
                    inputStream.close();
                } catch (IOException e) {
                    System.out.println("Failed to close keystore file: " + e);
                }
            }
        }


        RestTemplate kerberosRestTemplate = new KerberosRestTemplate(keytabLocation, kerberosUser, httpClient);

        List<String> classArgs = new ArrayList<String>();
        classArgs.add("100");

        SparkRequest sparkRequest = SparkRequest.builder()
                .className("org.apache.spark.examples.SparkPi")
                .driverMemory("1G")
                .driverCores(1)
                .executorCores(1)
                .executorMemory("1G")
                .numExecutors(1)
                .queue("default")
                .args(classArgs)
                .name("Livy_Keytab_Example")
                .proxyUser("yang.wang")
                .file("hdfs:///user/yang.wang/parking/examples.jar")
                .build();

        ObjectWriter ow = new ObjectMapper().writer().withDefaultPrettyPrinter();

        String sparkRequestJson = null;
        try {
            sparkRequestJson = ow.writeValueAsString(sparkRequest);
            System.out.println("sparkRequestJson:" + sparkRequestJson);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }

        System.out.println("Submitting Request to Livy");

        String livyURL = "https://ip-10-0-10-133.amer.o9solutions.local:8999/batches";

        kerberosRestTemplate.postForObject(livyURL, sparkRequestJson, String.class);

        System.out.println("Submitting Request to Livy Completed");

    }
}
