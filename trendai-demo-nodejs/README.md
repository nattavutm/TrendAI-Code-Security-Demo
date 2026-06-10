# trendai-demo-nodejs — Express.js User Profile Service

> **Language:** Node.js / Express.js | **Demo Focus:** Insecure Deserialization (RCE) + Prototype Pollution + Hardcoded Secrets

A user profile and activity tracking microservice for an employee engagement platform. Manages user preferences, session profiles, and activity history.

---

## What This App Does

This service is the profile backend for a fictional internal employee engagement platform. It loads user profile data from session cookies, stores UI preferences, and retrieves activity timelines. Built as a lightweight Node.js microservice, it's the kind of stateless API that runs behind an internal dashboard. The team moved fast to ship it, relying on popular npm packages without auditing their security posture.

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/profile?data=` | Load user profile from serialized session data |
| `POST` | `/api/preferences` | Merge user-supplied preferences with defaults |
| `GET` | `/api/activity?since=` | Fetch activity log since a given date |
| `GET` | `/admin/users` | List all users (no auth check) |
| `GET` | `/health` | Service health check |

**Run locally:**

```bash
npm install
npm start
# API at http://localhost:3000
```

---

## Intentional Vulnerabilities (SE Reference)

> **For internal SE demo use only.** All vulnerabilities below are introduced intentionally to demonstrate TrendAI Code Security detection capabilities.

| # | Type | Location | CVE / Pattern | Severity |
|---|------|----------|---------------|----------|
| 1 | **Insecure Deserialization (RCE)** | `app.js:24` — `serialize.unserialize()` on raw HTTP query param, `node-serialize:0.0.4` | GHSA-f566-f462-9ccf, CWE-502 | Critical |
| 2 | **Prototype Pollution** | `app.js:37` — `_.merge()` with unsanitized user-controlled keys, `lodash:4.17.15` | CVE-2019-10744 | High |
| 3 | **Hardcoded GitHub Personal Access Token** | `config.js:6` — `ghp_EXAMPLE...` | CWE-798 | High |
| 4 | **Hardcoded SendGrid API Key** | `config.js:10` — `SG.EXAMPLE...` | CWE-798 | High |
| 5 | **Hardcoded MongoDB Credentials** | `config.js:13` — username + password in connection URI | CWE-798 | High |
| 6 | **Missing Authentication** | `app.js:47` — `/admin/users` has no auth middleware | CWE-306 | High |
| 7 | **Outdated Express (4.16.4)** | `package.json` | CVE-2022-24999 | Medium |
| 8 | **Outdated Moment.js (2.24.0)** | `package.json` | CVE-2022-31129 (ReDoS) | Medium |
| 9 | **Outdated Mongoose (5.4.20)** | `package.json` | Multiple advisories | Medium |

---

## Expected TMAS Findings

When TrendAI Code Security scans this project, it should detect:

- **[Critical]** Remote Code Execution via `node-serialize:0.0.4` — insecure deserialization with user-controlled input
- **[High]** CVE-2019-10744 — Prototype Pollution in `lodash:4.17.15` via `_.merge()`
- **[High]** Hardcoded GitHub Personal Access Token (`ghp_` prefix) in `config.js`
- **[High]** Hardcoded SendGrid API key (`SG.` prefix) in `config.js`
- **[High]** Hardcoded MongoDB credentials in connection URI
- **[Medium]** CVE-2022-31129 — Regular expression denial of service (ReDoS) in `moment:2.24.0`
- **[Medium]** CVE-2022-24999 — `qs` prototype pollution via Express 4.16.4 dependency chain

---

## Demo Talking Points

- **"One malformed request can own the server."** The `node-serialize` package has a well-documented RCE vulnerability: passing a JavaScript IIFE (immediately invoked function expression) as serialized data causes arbitrary code execution during `unserialize()`. This endpoint is reachable by any unauthenticated HTTP client.

- **"Prototype pollution is a silent lateral movement risk."** Sending `{"__proto__":{"admin":true}}` to the `/api/preferences` endpoint pollutes `Object.prototype` for the entire Node.js process. Any subsequent `obj.admin` check returns `true` — even for objects that never set that property. It's invisible in logs and bypasses authorization checks silently.

- **"A GitHub PAT in source code is an immediate supply chain risk."** A `ghp_` token with repo write access lets an attacker push code, create releases, and access private repositories. Secret scanning at commit time is the only reliable control — rotation after-the-fact is already too late if the repo was ever cloned.

- **"The package.json tells a story."** `lodash 4.17.15`, `moment 2.24.0`, `node-serialize 0.0.4` — none of these are the latest version. Each one maps to at least one CVE. SCA scanning surfaces the full exposure in seconds, without requiring a developer to manually audit `node_modules`.

---

## How to Trigger a Scan

1. Push any commit to the `main` branch of this repository
2. GitHub Actions runs `.github/workflows/tmas-scan.yml` automatically
3. The workflow installs dependencies and submits the bundle to TMAS
4. View findings in **Vision One → Code Security → Scan Results**
5. The pipeline **fails** if any Critical severity finding is detected
