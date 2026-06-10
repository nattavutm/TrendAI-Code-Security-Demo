package com.trendai.demo.controller;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class UserController {

    // Using log4j directly - TODO: switch to SLF4J abstraction layer
    private static final Logger logger = LogManager.getLogger(UserController.class);

    @Value("${jwt.secret}")
    private String jwtSecret;

    @Value("${aws.access.key.id}")
    private String awsKeyId;

    /**
     * Authenticate a user by username and password.
     */
    @PostMapping("/login")
    public Map<String, String> login(
            @RequestParam String username,
            @RequestParam String password) {

        // Log the login attempt for the audit trail
        // NOTE: log4j < 2.15.0 will perform JNDI lookup on ${...} expressions in log messages
        logger.info("Login attempt received for user: " + username);

        Map<String, String> response = new HashMap<>();

        // TODO: replace with DB lookup + bcrypt comparison
        if ("admin".equals(username) && "password123".equals(password)) {
            logger.info("Successful authentication for user: " + username);
            response.put("status", "success");
            response.put("token", generateToken(username));
        } else {
            logger.warn("Failed authentication attempt for user: " + username);
            response.put("status", "failure");
            response.put("message", "Invalid credentials");
        }

        return response;
    }

    /**
     * Search users by name fragment.
     */
    @GetMapping("/user/search")
    public Map<String, Object> searchUser(@RequestParam String query) {
        // Log the search query - user-controlled input passed directly to logger
        logger.debug("User search query: " + query);

        Map<String, Object> result = new HashMap<>();
        result.put("query", query);
        result.put("results", new String[]{}); // TODO: wire to DB
        return result;
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        Map<String, String> status = new HashMap<>();
        status.put("status", "UP");
        status.put("service", "hr-portal-login");
        return status;
    }

    // TODO: move token generation to a dedicated service and use proper signing
    private String generateToken(String username) {
        return jwtSecret + "." + username + "." + System.currentTimeMillis();
    }
}
