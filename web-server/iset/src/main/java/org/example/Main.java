package org.example;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class Main {

    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
    }

    @GetMapping("/")
    public String hello() {
        return "Hello World!";
    }

    @GetMapping("/add")
    public String add(@RequestParam("a") int a, @RequestParam("b") int b) {
        int sum = a + b;
        for (int i=0; i<2000000; i++) {
            sum ^= a+b;
            sum *= 10;
        }
        return "Result is " + sum;
    }

    @GetMapping("/encode")
    public String encode(@RequestParam("a") int a) {
        try {
            String input = String.valueOf(a);
            MessageDigest digest = MessageDigest.getInstance("SHA-256");

            byte[] hashBytes = digest.digest(input.getBytes());

            StringBuilder hexString = new StringBuilder();
            for (byte hashByte : hashBytes) {
                String hex = Integer.toHexString(0xff & hashByte);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }

            return "SHA-256 Result: " + hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            return "SHA-256 cannot be initialized！";
        }
    }

    @GetMapping("col")
    public String col() {
        int sz = 10000;
        long [][] res = new long[sz][sz];
        for (int j=0; j<sz; j++) {
            for (int i=0; i<sz; i++) {
                res[i][j] = System.currentTimeMillis();
            }
        }

        return Long.toString(res[sz/2][sz/2] - res[sz/4][sz/4]);
    }
}
