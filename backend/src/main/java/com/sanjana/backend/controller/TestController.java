package com.sanjana.backend.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {

    @GetMapping("/check-ai")
    public String checkAI() {
        return "{\"status\":\"AI service is running\"}";
    }

    @GetMapping("/secure/test")
    public String secureTest() {
        return "Secure endpoint accessed";
    }
}