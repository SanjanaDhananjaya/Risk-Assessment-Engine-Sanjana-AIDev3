# Security Documentation

## 📅 Day 1 – OWASP Top 10 (2021)

### A01: Broken Access Control
**Attack Scenario:**  
An attacker modifies API requests to access restricted endpoints (e.g., accessing admin data without authorization).

**Impact:**  
Unauthorized data access and privilege escalation.

**Mitigation:**  
- Enforce role-based access control (RBAC)  
- Validate permissions on every request  

---

### A02: Cryptographic Failures
**Attack Scenario:**  
Sensitive data (API keys, tokens) is transmitted or stored without encryption.

**Impact:**  
Data leakage and compromise of system integrity.

**Mitigation:**  
- Use HTTPS (TLS 1.2+)  
- Encrypt sensitive data at rest  
- Avoid exposing secrets in logs  

---

### A03: Injection
**Attack Scenario:**  
User input like `DROP TABLE users` is processed without validation.

**Impact:**  
Database manipulation or unauthorized execution.

**Mitigation:**  
- Input sanitization  
- Parameterized queries  

---

### A04: Insecure Design
**Attack Scenario:**  
System lacks validation layers for user input or trust boundaries.

**Impact:**  
Architectural weaknesses leading to multiple vulnerabilities.

**Mitigation:**  
- Apply secure design principles  
- Threat modeling during development  

---

### A05: Security Misconfiguration
**Attack Scenario:**  
Default configurations expose debug endpoints or stack traces.

**Impact:**  
Information leakage and system compromise.

**Mitigation:**  
- Disable debug mode in production  
- Use secure headers  

---

### A06: Vulnerable and Outdated Components
**Attack Scenario:**  
Using outdated libraries with known vulnerabilities.

**Impact:**  
Exploitation of known security flaws.

**Mitigation:**  
- Regular dependency updates  
- Use vulnerability scanners  

---

### A07: Identification and Authentication Failures
**Attack Scenario:**  
Weak authentication allows brute-force login attempts.

**Impact:**  
Account takeover.

**Mitigation:**  
- Strong password policies  
- Rate limiting (already implemented)  

---

### A08: Software and Data Integrity Failures
**Attack Scenario:**  
Untrusted updates or dependencies are executed.

**Impact:**  
System compromise.

**Mitigation:**  
- Use signed dependencies  
- Validate integrity of data  

---

### A09: Security Logging and Monitoring Failures
**Attack Scenario:**  
No logging of suspicious activities.

**Impact:**  
Delayed detection of attacks.

**Mitigation:**  
- Implement structured logging  
- Monitor anomalies  

---

### A10: Server-Side Request Forgery (SSRF)
**Attack Scenario:**  
Attacker tricks server into making internal API calls.

**Impact:**  
Access to internal services.

**Mitigation:**  
- Validate outgoing requests  
- Restrict internal network access  

---

## 📅 Day 2 – Tool-Specific Threats

### 1. Groq API Key Leakage
**Attack Scenario:**  
API key exposed via `.env`, logs, or Git commits.

**Impact:**  
Unauthorized usage of AI services.

**Mitigation:**  
- Store keys in environment variables  
- Use secret managers  
- Add `.env` to `.gitignore`  

---

### 2. RAG Context Injection
**Attack Scenario:**  
Malicious content stored in vector DB manipulates LLM output.

**Impact:**  
Incorrect risk analysis decisions.

**Mitigation:**  
- Validate data before ingestion  
- Apply content filtering  

---

### 3. Vector Store Poisoning (ChromaDB)
**Attack Scenario:**  
Attacker injects misleading data into vector database.

**Impact:**  
Corrupted model responses.

**Mitigation:**  
- Restrict write access  
- Verify data sources  

---

### 4. LLM Hallucination Risk
**Attack Scenario:**  
Model generates incorrect outputs despite valid input.

**Impact:**  
Incorrect decision-making.

**Mitigation:**  
- Add confidence scoring  
- Use rule-based validation fallback  

---

### 5. JWT Token Theft / Replay
**Attack Scenario:**  
Captured token reused for unauthorized access.

**Impact:**  
Session hijacking.

**Mitigation:**  
- Short token expiry  
- HTTPS enforcement  
- Token rotation  

---

### 6. Cross-Service Attack (Backend ↔ AI Service)
**Attack Scenario:**  
Malicious request exploits communication between services.

**Impact:**  
Unauthorized data flow.

**Mitigation:**  
- Validate inter-service requests  
- Use authentication between services  

---

### 7. Prompt Injection via User Input
**Attack Scenario:**  
Input manipulates LLM behavior.

**Impact:**  
Unexpected outputs.

**Mitigation:**  
- Strict input filtering  
- Context isolation  

---

### 8. Data Leakage via Logs
**Attack Scenario:**  
Sensitive data logged in plaintext.

**Impact:**  
Exposure of confidential information.

**Mitigation:**  
- Mask sensitive fields  
- Secure logging practices  

---

### 9. API Abuse (AI Endpoint)
**Attack Scenario:**  
Repeated requests overload system.

**Impact:**  
Denial of service.

**Mitigation:**  
- Rate limiting (already implemented)  
- API authentication  

---

### 10. Dependency Supply Chain Attack
**Attack Scenario:**  
Compromised library injected into project.

**Impact:**  
System compromise.

**Mitigation:**  
- Use trusted sources  
- Verify package integrity  

---

## 📅 Day 3 – Input Sanitization

- HTML stripping using regex  
- SQL keyword detection  
- Prompt injection blocking  

**Result:**  
- Malicious input → **400 Bad Request**

---

## 📅 Day 4 – Rate Limiting

- Implemented using Flask-Limiter  
- Limits requests per IP  

**Result:**  
- Excess requests → **429 Too Many Requests**

---

## 📅 Day 5 – Security Testing

Tested:
- Empty input  
- Injection payloads  
- Edge cases  

All passed successfully.

---

## 📅 Day 6 – Backend Integration

- Flask AI service integrated with Spring Boot  
- REST communication established  

---

## 📅 Day 7 – OWASP ZAP Baseline Scan

- Identified missing headers  
- Initial vulnerabilities recorded  

---

## 📅 Day 8 – Security Headers Fix

Headers added:
- X-Content-Type-Options  
- X-Frame-Options  
- CSP  

---

## 📅 Day 9 – PII Protection

Blocked:
- Emails  
- Phone numbers  
- Aadhaar-like data  

---

## 📅 Day 10 – Validation

Verified:
- Headers present  
- Rate limiting working  
- Injection blocked  

---

## 📅 Day 11 – ZAP Active Scan

- Full scan executed  
- Fixed all **Critical and High** issues  

---

## 📅 Day 12 – Final Hardening

- Implemented Flask-Talisman  
- Re-scan shows **0 High/Critical**

---

## 📅 Day 13 – Full Stack Security Testing

| Test | Result |
|------|--------|
| No Token | 401 |
| Wrong Role | 403 |
| Injection | 400 |
| Rate Limit | 429 |

---

## 📅 Day 16 – Security Talking Points

- JWT Authentication  
- Rate Limiting  
- Input Sanitization  
- ZAP Results  

---

## 📅 Day 17 – Practice

- Individual explanation  
- Security flow rehearsed  

---

## 📅 Day 18 – Final Submission

- Documentation finalized  
- Ready for Demo  

---

## 🔐 Final Security Status

| Category | Status |
|--------|--------|
| Authentication | ✅ |
| Authorization | ✅ |
| Sanitization | ✅ |
| Rate Limiting | ✅ |
| ZAP Scan | ✅ Clean |

---

## 📌 Residual Risks

- No production JWT system  
- Local testing only  
- No HTTPS deployment  

---

## ✅ Final Sign-Off

✔ All tasks completed  
✔ System secured  
✔ Ready for demonstration  

---