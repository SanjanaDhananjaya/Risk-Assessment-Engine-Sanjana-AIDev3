package com.sanjana.backend.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.client.SimpleClientHttpRequestFactory;

@Service
public class AiServiceClient {

    private final RestTemplate restTemplate;

    public AiServiceClient() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(10000);
        factory.setReadTimeout(10000);

        this.restTemplate = new RestTemplate(factory);
    }

    public String checkAIService() {
        try {
            return restTemplate.getForObject("http://localhost:5000/test", String.class);
        } catch (Exception e) {
            return null; // graceful failure
        }
    }
}