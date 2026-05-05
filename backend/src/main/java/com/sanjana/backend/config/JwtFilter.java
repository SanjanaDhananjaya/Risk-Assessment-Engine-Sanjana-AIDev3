package com.sanjana.backend.config;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import java.io.IOException;

public class JwtFilter implements Filter {

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;

        String authHeader = request.getHeader("Authorization");

        // ❌ No token → 401
        if (authHeader == null || !authHeader.equals("Bearer valid-token")) {
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            response.getWriter().write("401 Unauthorized");
            return;
        }

        String role = request.getHeader("Role");

        // ❌ Wrong role → 403
        if (role == null || !role.equals("ADMIN")) {
            response.setStatus(HttpServletResponse.SC_FORBIDDEN);
            response.getWriter().write("403 Forbidden");
            return;
        }

        // ✅ Valid
        chain.doFilter(req, res);
    }
}