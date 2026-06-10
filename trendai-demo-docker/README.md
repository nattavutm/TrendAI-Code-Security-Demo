# trendai-demo-docker — Containerized Flask Data Ingestion Service

> **Language:** Python / Docker | **Demo Focus:** Container Image Secrets + EOL Base Image + Malware Behavior Pattern

A containerized Flask microservice for an internal data ingestion pipeline. Packaged as a Docker image and deployed on the internal Kubernetes cluster.

---

## What This App Does

This service is a containerized backend for a data ingestion pipeline — it receives payloads, processes them, and pushes results to downstream storage (S3 and GCS). It was Dockerized by the DevOps team for consistency across environments and deployed to a private Kubernetes namespace. Secrets were bundled into the image during an early iteration and the team never got around to migrating them to Kubernetes secrets. The startup script also contains some leftover automation code from an infra sprint that was never cleaned up.

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Container health check / liveness probe |
| `GET` | `/api/data` | Retrieve latest ingested pipeline data |
| `GET` | `/api/echo?msg=` | Echo utility for testing |

**Run locally:**

```bash
docker build -t trendai-demo-docker .
docker run -p 5000:5000 trendai-demo-docker
# API at http://localhost:5000
```

---

## Intentional Vulnerabilities (SE Reference)

> **For internal SE demo use only.** All vulnerabilities below are introduced intentionally to demonstrate TrendAI Code Security detection capabilities.

| # | Type | Location | CVE / Pattern | Severity |
|---|------|----------|---------------|----------|
| 1 | **Secrets Baked into Docker Image Layer** | `Dockerfile:7` — `.env` file COPY'd into image; persists in all layer snapshots even if later deleted | CWE-540 | Critical |
| 2 | **Hardcoded AWS Access Key** | `.env:4-5` — `AKIAIOSFODNN7EXAMPLE` + secret key | CWE-798 | Critical |
| 3 | **Hardcoded GCP Service Account Key** | `.env:9` — full private key JSON in plaintext | CWE-798 | Critical |
| 4 | **Hardcoded SSH Private Key** | `.env:13-16` — RSA PEM block in plaintext | CWE-312 | Critical |
| 5 | **Outbound Beacon on Startup** | `startup.sh:14` — `curl` to hardcoded external IP `198.51.100.42` at container start | CWE-506 | Critical |
| 6 | **Base64-Encoded Payload Execution** | `startup.sh:17-18` — encoded string decoded and piped to `bash` at startup | CWE-506 | Critical |
| 7 | **End-of-Life Base Image** | `Dockerfile:2` — `python:3.6-slim` (EOL Dec 2021, unpatched OS CVEs) | CWE-1395 | High |
| 8 | **Container Runs as Root** | `Dockerfile` — no `USER` directive; process runs as UID 0 | CWE-250 | High |
| 9 | **Outdated Flask (1.0.2)** | `requirements.txt:2` | CVE-2018-1000656 | High |
| 10 | **Outdated Werkzeug (0.14.1)** | `requirements.txt:3` | CVE-2019-14806 | Medium |

---

## Expected TMAS Findings

When TrendAI Code Security scans this Docker image, it should detect:

- **[Critical]** AWS Access Key ID and Secret baked into image layer (found in `.env` copied during build)
- **[Critical]** GCP Service Account private key material in plaintext within image filesystem
- **[Critical]** SSH RSA private key stored in plaintext within image filesystem
- **[Critical]** Malware behavior indicator — outbound network beacon to external IP in startup script
- **[Critical]** Malware behavior indicator — base64-encoded payload executed via `bash` at container start
- **[High]** End-of-life OS base (`python:3.6-slim`) with unpatched CVEs in OS packages
- **[High]** Container process runs as root (UID 0)
- **[High]** CVE-2018-1000656 — Flask 1.0.2 vulnerability
- **[Medium]** CVE-2019-14806 — Werkzeug 0.14.1 predictable temp file names

---

## Demo Talking Points

- **"Deleting the .env file doesn't remove it from the image."** Even if the developer adds a `RUN rm .env` step after the `COPY`, the `.env` contents are permanently preserved in the intermediate layer. Anyone who pulls the image can run `docker history` or extract the layer tarball to retrieve the secrets. TMAS image layer scanning detects this even after deletion.

- **"The startup script looks like ransomware staging."** The combination of an outbound beacon call + base64-encoded payload piped to `bash` is a textbook malware pattern — it's how real attackers establish persistence and pull down second-stage payloads. TrendAI's behavioral analysis flags this pattern regardless of what the payload actually does.

- **"EOL base images are a silent debt."** `python:3.6-slim` reached end-of-life in December 2021. Every container built from it inherits all unpatched CVEs in the underlying OS packages — packages the app team doesn't even know exist. TMAS OS layer scanning enumerates every package in the base image and maps each one to the CVE database.

- **"Running as root amplifies every other vulnerability."** Without a `USER` directive, the Flask process runs as UID 0. If any vulnerability in this container is exploited, the attacker immediately has root access inside the container — and potentially a path to container escape. This is a one-line Dockerfile fix that TMAS flags with high severity.

---

## How to Trigger a Scan

1. Push any commit to the `main` branch of this repository
2. GitHub Actions runs `.github/workflows/tmas-scan.yml` automatically
3. The workflow builds the Docker image with `docker build` and submits it to TMAS for image scanning
4. View findings in **Vision One → Code Security → Scan Results**
5. The pipeline **fails** if any Critical severity finding is detected
