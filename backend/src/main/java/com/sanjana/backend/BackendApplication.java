package com.sanjana.backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;

import com.sanjana.backend.config.SecurityHeadersConfig;
import com.sanjana.backend.config.JwtFilter;

@SpringBootApplication
public class BackendApplication {

    public static void main(String[] args) {
        SpringApplication.run(BackendApplication.class, args);
    }

    // 🔐 Register Security Headers Filter (CRITICAL for ZAP)
    @Bean
    public FilterRegistrationBean<SecurityHeadersConfig> securityHeadersFilter() {
        FilterRegistrationBean<SecurityHeadersConfig> registrationBean = new FilterRegistrationBean<>();

        registrationBean.setFilter(new SecurityHeadersConfig());
        registrationBean.addUrlPatterns("/*"); // Apply to ALL endpoints
        registrationBean.setOrder(1); // Runs first

        return registrationBean;
    }

    // 🔑 Register JWT Filter (for secured endpoints only)
    @Bean
    public FilterRegistrationBean<JwtFilter> jwtFilter() {
        FilterRegistrationBean<JwtFilter> registrationBean = new FilterRegistrationBean<>();

        registrationBean.setFilter(new JwtFilter());
        registrationBean.addUrlPatterns("/secure/*"); // Apply ONLY to secure endpoints
        registrationBean.setOrder(2); // Runs after security headers

        return registrationBean;
    }
}