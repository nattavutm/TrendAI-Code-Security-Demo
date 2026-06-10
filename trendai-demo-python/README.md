# trendai-demo-python — Flask Employee Directory Service

> **Language:** Python 3 / Flask | **Demo Focus:** SQL Injection + RCE Backdoor + Hardcoded Secrets + Outdated SCA

A lightweight user management and authentication service for an internal employee directory. Supports login, user search, and an admin diagnostic panel.

---

## What This App Does

This service powers a fictional internal employee directory — a simple web app that lets HR staff log in, search for colleagues, and manage user records. An admin panel provides diagnostic tools for the ops team. Built quickly as an internal tool, it uses a SQLite database and minimal dependencies. The kind of app that starts as a weekend project and ends up running in production for three years.

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/login` | Authenticate user against database |
| `GET` | `/api/users?search=` | Search users by name |
| `GET/POST` | `/admin/exec?cmd=` | Admin diagnostic shell command runner |
| `POST` | `/admin/upload` | File upload utility |
| `GET` | `/health` | Service health check |

**Run locally:**

```bash
pip install -r requirements.txt
python app.py
# API at http://localhost:5000
```

---

## Intentional Vulnerabilities (SE Reference)

> **For internal SE demo use only.** All vulnerabilities below are introduced intentionally to demonstrate TrendAI Code Security detection capabilities.

| # | Type | Location | CVE / Pattern | Severity |
|---|------|----------|---------------|----------|
| 1 | **OS Command Injection (RCE)** | `app.py:49` — `os.popen(cmd)` with no authentication or input sanitization | CWE-78 | Critical |
| 2 | **SQL Injection (Auth Bypass)** | `app.py:33` — login query built with f-string, no parameterization | CWE-89 | Critical |
| 3 | **SQL Injection (Data Exfiltration)** | `app.py:42` — search query built with f-string | CWE-89 | High |
| 4 | **Hardcoded Stripe API Key** | `config.py:5` — `sk_live_EXAMPLE...` | CWE-798 | High |
| 5 | **Hardcoded Admin Password** | `config.py:12` — `admin123` in plaintext source | CWE-798 | High |
| 6 | **Hardcoded Slack Webhook URL** | `config.py:8` — full webhook URL in source | CWE-798 | High |
| 7 | **Outdated Flask (0.12.2)** | `requirements.txt:2` | CVE-2018-1000656 | High |
| 8 | **Outdated Werkzeug (0.14.1)** | `requirements.txt:3` | CVE-2019-14806 | Medium |
| 9 | **Outdated Pillow (5.0.0)** | `requirements.txt:4` | CVE-2019-16865, CVE-2020-5313 | Medium |
| 10 | **Path Traversal in Upload** | `app.py:57` — `f.filename` used unsanitized in `os.path.join` | CWE-22 | Medium |

---

## Expected TMAS Findings

When TrendAI Code Security scans this project, it should detect:

- **[Critical]** Hardcoded Stripe secret key (`sk_live_` prefix) in `config.py`
- **[Critical]** OS Command Injection pattern — `os.popen()` with unvalidated HTTP parameter in `app.py`
- **[High]** SQL Injection in login and search endpoints — f-string query construction
- **[High]** Hardcoded admin credentials in source code
- **[High]** Hardcoded Slack webhook URL
- **[High]** CVE-2018-1000656 — Flask 0.12.2 denial of service via malformed JSON
- **[Medium]** CVE-2019-14806 — Werkzeug 0.14.1 predictable temporary file names
- **[Medium]** Multiple Pillow 5.0.0 image parsing CVEs (CVE-2019-16865, CVE-2020-5313)

---

## Demo Talking Points

- **"This is a backdoor, not just a bug."** The `/admin/exec` endpoint accepts any shell command via an HTTP GET parameter with no authentication — a developer left it in for "debugging." This is the exact pattern used in web shells deployed by attackers after initial compromise. TrendAI detects this as a malicious code pattern, not just a misconfiguration.

- **"SQL injection is still the number one web vulnerability."** Using `f"SELECT * FROM users WHERE username = '{username}'"` means sending `' OR '1'='1` as the username bypasses login entirely. Parameterized queries are a one-line fix — but TrendAI catches it before that fix is even needed.

- **"The Stripe key is live — or was."** A `sk_live_` prefix means this key has real payment processing permissions. Once it's in a git repository — even a private one — it should be considered compromised. Code Security flags this at the commit level so the key can be rotated immediately.

- **"Outdated packages create an invisible attack surface."** Flask 0.12.2 and Pillow 5.0.0 are years past their end-of-life. Teams using them often don't know because `pip install` succeeded. SCA scanning maps the exact installed versions to the CVE database and shows the upgrade path.

---

## How to Trigger a Scan

1. Push any commit to the `main` branch of this repository
2. GitHub Actions runs `.github/workflows/tmas-scan.yml` automatically
3. The workflow bundles the application and submits it to TMAS
4. View findings in **Vision One → Code Security → Scan Results**
5. The pipeline **fails** if any Critical severity finding is detected
