package org.example;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

import java.io.FileWriter;
import java.io.BufferedWriter;
import java.io.IOException;

@Aspect
@Component
public class RequestTimeAspect {

    @Around("execution(* org.example.Main.*(..))")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long startTime = System.currentTimeMillis();

        Object proceed = joinPoint.proceed();

        long endTime = System.currentTimeMillis();
        long totalTime = endTime - startTime;

        System.out.println("Method execution time: " + totalTime + " milliseconds");

        try (FileWriter fileWriter = new FileWriter("execution_time.log", true);
            BufferedWriter bufferedWriter = new BufferedWriter(fileWriter)) {
            bufferedWriter.write("Method execution time: " + totalTime + " milliseconds");
            bufferedWriter.newLine();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return proceed;
    }
}
