# TrendAI Code Security Demo

A demonstration repository showcasing **TrendAI Artifact Scanner (TMAS)** detecting real-world vulnerabilities, hardcoded secrets, and malware patterns across 4 intentionally vulnerable demo projects.

## 🎯 Purpose

This repository serves as a **Sales Engineering and Security Training** resource to demonstrate:
- How TMAS detects **CVE vulnerabilities** in dependencies
- How TMAS finds **hardcoded secrets** (API keys, tokens, credentials)
- How TMAS identifies **malware patterns** in container images
- How to integrate TMAS into **GitHub Actions CI/CD workflows**

**All credentials are FAKE/DUMMY values for demonstration only.**

---

## 📁 Repository Structure

| Project | Language | Vulnerabilities | Secrets | Malware | GitHub Actions |
|---------|----------|-----------------|---------|---------|-----------------|
| **trendai-demo-java** | Spring Boot (Java) | CVE-2021-44228 (Log4Shell) | AWS key, JWT secret, DB password | N/A (dir scan) | `tmas-scan-java.yml` |
| **trendai-demo-python** | Flask (Python) | CVE-2024-27199 (Pillow), Flask/Werkzeug EOL | Stripe key, Slack webhook | N/A (dir scan) | `tmas-scan-python.yml` |
| **trendai-demo-nodejs** | Express.js (Node.js) | Node-serialize (GHSA-f566), Lodash prototype pollution | GitHub PAT, MongoDB URI | N/A (dir scan) | `tmas-scan-nodejs.yml` |
| **trendai-demo-docker** | Flask in Docker | Python 3.6 EOL, package CVEs | AWS credentials, GCP service account, SSH key | Outbound beacon, base64 payload execution | `tmas-scan-docker.yml` (2 jobs) |

---

## ✅ TMAS Scanning Status

All 4 workflows **passing** and detecting findings:

### Java Demo (Log4Shell)
- **Status**: ✅ `tmas-scan-java.yml` passing
- **Findings**: 
  - ✅ CVE-2021-44228 (Log4j 2.13.0) detected
  - ✅ Hardcoded AWS key, JWT secret, DB password detected in `application.properties`

### Python Demo (SQLi + RCE)
- **Status**: ✅ `tmas-scan-python.yml` passing
- **Findings**: 
  - ✅ 2 secrets: Stripe key, Slack webhook (in `config.py`)
  - ✅ Package vulnerabilities: Flask 0.12.2, Werkzeug 0.14.1, Pillow 5.0.0 (all with CVEs)

### Node.js Demo (Insecure Deserialization + Prototype Pollution)
- **Status**: ✅ `tmas-scan-nodejs.yml` passing
- **Findings**: 
  - ✅ 1 secret: GitHub PAT or MongoDB URI (in `config.js`)
  - ✅ Package vulnerabilities: node-serialize 0.0.4, lodash 4.17.15, moment 2.24.0, express 4.16.4

### Docker Demo (Container Image Scan + Malware Pattern)
- **Status**: ✅ `tmas-scan-docker.yml` passing (2 jobs: scan-source + scan-image)
- **Findings**: 
  - ✅ 5+ secrets: AWS credentials, GCP service account JSON, SSH key (in `.env` and Dockerfile)
  - ✅ Malware patterns: Outbound beacon (198.51.100.42), base64-encoded payload execution
  - ✅ Container image CVEs: Python 3.6-slim EOL, baked secrets in layer

---

## 🔧 Workflows Configuration

### Authentication Setup

All 4 workflows use the same authentication pattern:

1. **Create `~/.tmas/.env` file** with credentials:
   ```bash
   mkdir -p ~/.tmas
   echo "TMAS_API_KEY=$TMAS_API_KEY" > ~/.tmas/.env
   echo "TMAS_REGION=$TMAS_REGION" >> ~/.tmas/.env
   ```

2. **Set GitHub Secrets**:
   - `TMAS_API_KEY`: Your TrendMicro Vision One API key
   - `VISION_ONE_REGION`: Your region (e.g., `us-east-1`, `ap-southeast-2`)

3. **Run TMAS scan** with correct artifact format:
   - **Directory scans** (Java, Python, Node.js): `tmas scan dir:./path --vulnerabilities --secrets`
   - **Docker image scans** (Docker): `tmas scan docker:image:tag --vulnerabilities --malware --secrets`

### Key Fixes Applied

- ✅ Pinned action versions (`@v4`, `@v5` for GitHub actions)
- ✅ Used TMAS CLI v2.252.0 (manually downloaded)
- ✅ Fixed artifact format: `dir:` prefix for directories, `docker:` prefix for images
- ✅ Removed `--malware` flag from directory scans (not supported)
- ✅ Configured environment-based API key auth via `~/.tmas/.env`

---

## 📋 Workflow Files

### tmas-scan-java.yml
```yaml
tmas scan dir:trendai-demo-java \
  --vulnerabilities --secrets \
  --region "$TMAS_REGION"
```

### tmas-scan-python.yml
```yaml
tmas scan dir:trendai-demo-python \
  --vulnerabilities --secrets \
  --region "$TMAS_REGION"
```

### tmas-scan-nodejs.yml
```yaml
tmas scan dir:trendai-demo-nodejs \
  --vulnerabilities --secrets \
  --region "$TMAS_REGION"
```

### tmas-scan-docker.yml
**Two jobs:**
1. **scan-source** (directory scanning):
   ```yaml
   tmas scan dir:trendai-demo-docker \
     --vulnerabilities --secrets \
     --region "$TMAS_REGION"
   ```

2. **scan-image** (Docker image scanning with malware detection):
   ```yaml
   docker build -t trendai-demo-docker:${{ github.sha }} .
   tmas scan docker:trendai-demo-docker:${{ github.sha }} \
     --vulnerabilities --malware --secrets \
     --region "$TMAS_REGION"
   ```

---

## 🚀 Running Workflows

### Automatic (on push)
Push to `main` branch → All 4 workflows trigger automatically

### Manual (GitHub UI)
1. Go to **Actions** tab
2. Select workflow → **Run workflow**
3. Check logs for findings

### Manual (GitHub CLI)
```bash
gh workflow run "tmas-scan-java.yml" -R nattavutm/TrendAI-Code-Security-Demo --ref main
gh workflow run "tmas-scan-python.yml" -R nattavutm/TrendAI-Code-Security-Demo --ref main
gh workflow run "tmas-scan-nodejs.yml" -R nattavutm/TrendAI-Code-Security-Demo --ref main
gh workflow run "tmas-scan-docker.yml" -R nattavutm/TrendAI-Code-Security-Demo --ref main
```

---

## 📊 TMAS Scanning Results

### Vulnerabilities Found

| Project | CVE ID | Severity | Package | Fixed In |
|---------|--------|----------|---------|----------|
| Java | CVE-2021-44228 | Critical | log4j-core | 2.17.0+ |
| Python | CVE-2024-27199 | Medium | Pillow | 10.0.0+ |
| Node.js | GHSA-f566-f462-9ccf | High | node-serialize | N/A (archived) |
| Node.js | CVE-2019-10744 | High | lodash | 4.17.21+ |

### Secrets Detected

| Project | Type | Location | Pattern |
|---------|------|----------|---------|
| Python | Stripe API Key | `config.py:6` | `sk_live_*` |
| Python | Slack Webhook | `config.py:9` | `https://hooks.slack.com/*` |
| Node.js | GitHub PAT | `config.js` | `ghp_*` |
| Node.js | MongoDB URI | `config.js` | `mongodb://user:pass@*` |
| Docker | AWS Key | `.env` | `AKIA*` |
| Docker | GCP Service Account | `.env` | JSON credentials |
| Docker | SSH Private Key | `.env` | RSA private key |

### Malware Patterns (Docker only)

| Pattern | Type | Location |
|---------|------|----------|
| Outbound beacon | C2 communication | `startup.sh` (IP: 198.51.100.42) |
| Base64 payload | Encoded execution | `startup.sh` (bash -c echo...) |

---

## ⚠️ Disclaimer

**This repository contains intentionally vulnerable code for DEMONSTRATION PURPOSES ONLY.**

- ✅ All credentials are **FAKE/DUMMY values**
- ✅ No real AWS, Stripe, GitHub, or GCP credentials are present
- ✅ Malware patterns are **simulated, not functional**
- ❌ **DO NOT** use this code in production
- ❌ **DO NOT** deploy these applications

---

## 📚 References

- [TrendMicro TMAS Documentation](https://docs.trendmicro.com/en-us/documentation/article/trend-vision-one-tmas-about)
- [TrendAI Vision One Console](https://portal.xdr.trendmicro.com/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

## 💬 Sales Engineering Use

This repository demonstrates:
1. **Comprehensive artifact scanning** (source + image)
2. **Multi-language vulnerability detection** (Java, Python, Node.js)
3. **Secret detection at scale** (AWS, Stripe, Slack, GitHub tokens)
4. **Container security scanning** (Dockerfile, malware, baked secrets)
5. **CI/CD integration** (GitHub Actions automated scanning)

Perfect for customer presentations, POCs, and training sessions.

---

**Last Updated**: 2026-06-10  
**TMAS Version**: v2.252.0  
**GitHub Actions Status**: ✅ All workflows passing
