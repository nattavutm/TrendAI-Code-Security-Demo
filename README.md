# TrendAI Code Security — Demo Repository

![For Demo Purposes Only](https://img.shields.io/badge/For%20Demo%20Purposes%20Only-critical?style=flat-square)
![Do Not Use in Production](https://img.shields.io/badge/Do%20Not%20Use%20In%20Production-orange?style=flat-square)
![TrendAI Code Security](https://img.shields.io/badge/TrendAI-Code%20Security-blue?style=flat-square)

A curated collection of intentionally vulnerable demo applications used to showcase **TrendAI Code Security** scanning capabilities across multiple languages, vulnerability categories, and scan types.

---

## Overview

This repository contains four purposely insecure applications built to demonstrate how **TrendAI Code Security** (powered by Trend Vision One) detects real-world security risks in source code, open-source dependencies, hardcoded secrets, and container images — before they reach production.

Each sub-project is a realistic but vulnerable app written by a "careless developer." Together they cover the three core threat categories that TrendAI Code Security addresses:

| Category | Description | Examples in This Repo |
|----------|-------------|-----------------------|
| **Vulnerabilities (CVE)** | Known CVEs in open-source dependencies detected via SCA | Log4Shell (CVE-2021-44228), lodash prototype pollution, outdated Flask / Pillow |
| **Hardcoded Secrets** | API keys and credentials committed directly to source code | AWS access keys, Stripe keys, GitHub PATs, SSH private keys, GCP service account JSON |
| **Malware / Backdoor Patterns** | Suspicious code patterns that mirror real-world threats | Base64-encoded payloads, unauthenticated OS command execution, outbound beacons |

---

## Repository Structure

| Folder | Language | Key Vulnerabilities | Demo Focus |
|--------|----------|---------------------|------------|
| [`trendai-demo-java`](./trendai-demo-java) | Java / Spring Boot | Log4Shell (CVE-2021-44228), hardcoded AWS key + JWT secret | CVE in dependency, secrets in properties file |
| [`trendai-demo-python`](./trendai-demo-python) | Python / Flask | SQL Injection, unauthenticated OS Command Injection, hardcoded Stripe key | Backdoor/RCE pattern, secrets scanning, SCA |
| [`trendai-demo-nodejs`](./trendai-demo-nodejs) | Node.js / Express | Insecure deserialization (RCE), prototype pollution, hardcoded GitHub PAT | Vulnerable package chain, secrets scanning |
| [`trendai-demo-docker`](./trendai-demo-docker) | Python / Docker | Secrets baked into image layer, EOL base image, malware-like startup script | Container image scanning, malware behavior |

---

## How to Use (SE Demo Guide)

### Step 1 — Connect this repo to Vision One Code Security
1. In **Trend Vision One**, navigate to **Code Security → Repositories**
2. Click **Connect Repository** and select GitHub
3. Authorize the Vision One GitHub App and select this repository

### Step 2 — Trigger a scan
- **Automatic:** Push any commit to `main` or open a Pull Request — the workflow triggers automatically
- **Manual:** Go to **Actions → TMAS Security Scan → Run workflow** in this GitHub repo

Each subdirectory has its own `.github/workflows/tmas-scan.yml` that builds the appropriate artifact and runs TMAS.

### Step 3 — View findings in Vision One
1. Open **Vision One → Code Security → Scan Results**
2. Filter by repository name and the latest commit SHA
3. Explore findings grouped by **Severity**, **Type**, and **File**

### Step 4 — Walk through each finding category
- **CVE findings:** Start with `trendai-demo-java` for Log4Shell — show the vulnerable `pom.xml` dep and the logging call in `UserController.java`. Then show `trendai-demo-nodejs` for lodash.
- **Hardcoded Secrets:** Open `application.properties`, `config.py`, `config.js`, and `.env` — show how secret scanning flags `AKIA`, `sk_live_`, `ghp_`, and `SG.` prefixes.
- **Malware Patterns:** Use `trendai-demo-docker` — highlight `startup.sh` with the outbound beacon and base64-encoded payload execution. Show that the `.env` secrets are baked into the Docker image layer.

### Step 5 — Demonstrate policy enforcement (pipeline blocking)
- Each workflow is configured to **fail the pipeline** (`exit 1`) if **any CRITICAL severity finding** is detected
- Navigate to **Actions → TMAS Security Scan** and show the failed run
- Explain how this gates a PR merge and prevents vulnerable code from reaching production

---

## GitHub Actions Setup

Each subdirectory workflow requires two **GitHub repository secrets**:

| Secret Name | Description | Where to Find It |
|-------------|-------------|-----------------|
| `TMAS_API_KEY` | TMAS authentication key | Vision One → Administration → API Keys → Generate Key |
| `VISION_ONE_REGION` | Your Vision One data residency region | Vision One → Administration → About (e.g. `us-east-1`, `eu-central-1`) |

**To configure secrets:**
1. Go to this GitHub repo → **Settings → Secrets and variables → Actions**
2. Click **New repository secret** and add both values

---

## Disclaimer

> **This repository is for authorized demonstration and internal SE testing purposes only.**
>
> - All credentials, API keys, tokens, and passwords in this repository are **intentionally fake** and do not grant access to any real systems.
> - The vulnerability patterns are designed to demonstrate detection capabilities — not to be used for actual attacks.
> - **Do not deploy any of these applications** to a production environment or expose them to the public internet.
> - This repository exists solely to demonstrate TrendAI Code Security scanning capabilities in a controlled demo environment.
