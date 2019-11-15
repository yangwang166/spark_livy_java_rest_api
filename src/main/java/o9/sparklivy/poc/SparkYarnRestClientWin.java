package o9.sparklivy.poc;

import java.io.IOException;
import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.List;

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


@Slf4j
public class SparkYarnRestClientWin {

    public static void main(String[] arguments) {

        // keberos
        Configuration conf = new Configuration();
        conf.set("hadoop.security.authentication", "Kerberos");

        UserGroupInformation.setConfiguration(conf);

        System.setProperty("java.security.auth.login.config", "true");
        System.setProperty("java.security.krb5.conf", "C:\\Windows\\krb5.ini");
        System.setProperty("sun.security.krb5.debug", "true");


        String kerberosUser = "yang.wang@AMER.O9SOLUTIONS.LOCAL";
        String keytabLocation = "C:\\yang2\\yangwang2.keytab";

        try {
            UserGroupInformation.loginUserFromKeytab(kerberosUser, keytabLocation);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        System.out.println("Auth Completed");

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        RestTemplate kerberosRestTemplate = new KerberosRestTemplate(keytabLocation, kerberosUser);

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

        String livyURL = "http://ip-10-0-10-133.amer.o9solutions.local:8999/batches";

        kerberosRestTemplate.postForObject(livyURL, sparkRequestJson, String.class);

        System.out.println("Submitting Request to Livy Completed");

    }
}
