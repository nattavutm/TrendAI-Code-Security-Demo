# TrendAI Code Security Demo

A hands-on demo repository for testing **TrendAI Artifact Scanner (TMAS)** — automatically scans 4 intentionally vulnerable projects for CVEs, hardcoded secrets, and malware patterns via GitHub Actions.

> ⚠️ **Disclaimer:** All credentials in this repository are **fake/dummy values** for demonstration purposes only. Do not use in production.

---

## 🎯 What This Demo Shows

This repository demonstrates how TMAS detects security issues across multiple languages and artifact types:

- ✅ **CVE Detection** — Known vulnerabilities in dependencies (Log4j, Lodash, Pillow, etc.)
- ✅ **Secret Detection** — Hardcoded API keys, tokens, passwords in source code
- ✅ **Malware Detection** — Suspicious patterns inside container images
- ✅ **CI/CD Integration** — Automated scanning on every push via GitHub Actions

---

## 📦 Demo Projects

| Project | Language | Demonstrates |
|---------|----------|--------------|
| `trendai-demo-java/` | Java (Spring Boot) | CVE-2021-44228 Log4Shell, hardcoded AWS/JWT credentials |
| `trendai-demo-python/` | Python (Flask) | SQL injection, Stripe key & Slack webhook leak |
| `trendai-demo-nodejs/` | Node.js (Express) | Prototype pollution, insecure deserialization, GitHub PAT leak |
| `trendai-demo-docker/` | Docker | Container layer secrets, malware behavior patterns (beacon, base64 payload) |

---

## 🚀 Quick Start

### Step 1 — Get Your API Key

1. Log in to [TrendAI Vision One Console](https://portal.xdr.trendmicro.com/)
2. Navigate to **Administration** → **User Roles**
3. Verify your role has **"Run artifact scan"** permission
4. Go to **Administration** → **API Keys**
5. Click **Add API Key** → assign the role → save
6. Copy the API key and note your region (e.g., `us-east-1`)

---

### Step 2 — Configure GitHub Secrets

In your forked repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add:

| Secret Name | Value |
|-------------|-------|
| `TMAS_API_KEY` | Your Vision One API key |
| `VISION_ONE_REGION` | Your region code (e.g., `us-east-1`, `ap-southeast-1`) |

**Supported regions:** `us-east-1`, `eu-central-1`, `eu-west-2`, `ca-central-1`, `ap-south-1`, `ap-northeast-1`, `ap-southeast-1`, `ap-southeast-2`, `me-central-1`

---

### Step 3 — Trigger the Scans

**Option A — GitHub UI:**
1. Open the **Actions** tab
2. Select a workflow (e.g., *TMAS Scan — Python*)
3. Click **Run workflow** → choose `main` branch → **Run**

**Option B — GitHub CLI:**
```bash
gh workflow run "tmas-scan-java.yml"   --ref main
gh workflow run "tmas-scan-python.yml" --ref main
gh workflow run "tmas-scan-nodejs.yml" --ref main
gh workflow run "tmas-scan-docker.yml" --ref main
```

**Option C — Push to main:**
Any push to the `main` branch automatically triggers all 4 workflows.

---

### Step 4 — Review the Results

**In GitHub Actions:**
1. Open the **Actions** tab → click on the workflow run
2. Click the job → expand the **Run TMAS Scan** step
3. Look at the JSON output:

```json
{
  "vulnerabilities": { ... }  // CVEs detected
  "secrets":         { ... }  // Hardcoded credentials
  "malware":         { ... }  // Suspicious patterns (Docker images only)
}
```

**In Vision One Console:**
1. Open [Vision One Console](https://portal.xdr.trendmicro.com/)
2. Navigate to **Code Security** → **Artifact Scanner**
3. View aggregated findings across all scans

---

## 🔍 What You'll Find

Each project intentionally contains realistic security issues for TMAS to detect:

| Project | Expected Vulnerability Findings | Expected Secret Findings |
|---------|----------------------------------|--------------------------|
| **Java** | log4j-core 2.13.0 (CVE-2021-44228) | AWS access key, JWT signing key, DB password |
| **Python** | Flask 0.12.2, Werkzeug 0.14.1, Pillow 5.0.0 | Stripe live key, Slack webhook URL |
| **Node.js** | node-serialize 0.0.4, lodash 4.17.15, express 4.16.4 | GitHub PAT, SendGrid API key, MongoDB URI |
| **Docker** | python:3.6-slim (EOL), package CVEs | AWS credentials, GCP service account, SSH private key |

The Docker workflow additionally scans the built **container image** for malware patterns (outbound beacon, base64-encoded payload).

---

## 🏗️ How It Works

```
┌──────────────┐
│ git push     │
│   to main    │
└──────┬───────┘
       ▼
┌──────────────────────────┐
│ GitHub Actions trigger    │
│ (4 workflows in parallel) │
└──────┬───────────────────┘
       ▼
┌──────────────────────────────────┐
│ Download TMAS CLI v2.252.0       │
│ Create ~/.tmas/.env with API key │
└──────┬───────────────────────────┘
       ▼
┌──────────────────────────────────────────┐
│  tmas scan <artifact> [scanners]         │
│                                          │
│  • dir:project    → vulnerabilities, secrets        │
│  • docker:image   → vulnerabilities, secrets, malware │
└──────┬───────────────────────────────────┘
       ▼
┌──────────────────────────────────┐
│  Results sent to Vision One      │
│  + JSON output in workflow log   │
└──────────────────────────────────┘
```

---

## 💻 Local Testing (Optional)

Test TMAS locally without GitHub Actions:

```bash
# 1. Download TMAS CLI (Linux)
curl -L "https://ast-cli.xdr.trendmicro.com/tmas-cli/latest/tmas-cli_Linux_x86_64.tar.gz" | tar xz

# macOS (Apple Silicon)
curl -L "https://ast-cli.xdr.trendmicro.com/tmas-cli/latest/tmas-cli_Darwin_arm64.zip" -o tmas.zip && unzip tmas.zip

# 2. Set credentials
export TMAS_API_KEY="your-api-key-here"
export TMAS_REGION="us-east-1"

# 3. Scan a directory
./tmas scan dir:trendai-demo-python --vulnerabilities --secrets --region $TMAS_REGION

# 4. Scan a Docker image (also detects malware)
docker build -t trendai-demo-docker:latest ./trendai-demo-docker
./tmas scan docker:trendai-demo-docker:latest --vulnerabilities --malware --secrets --region $TMAS_REGION
```

---

## 🧰 Workflow Files

All workflows live in `.github/workflows/`:

| File | What It Does |
|------|--------------|
| `tmas-scan-java.yml` | Builds Maven project + scans `dir:trendai-demo-java` |
| `tmas-scan-python.yml` | Scans `dir:trendai-demo-python` directly |
| `tmas-scan-nodejs.yml` | Scans `dir:trendai-demo-nodejs` directly |
| `tmas-scan-docker.yml` | 2 jobs — scans source directory + builds & scans Docker image |

**Important notes:**
- `--malware` flag works only with image artifacts (`docker:`, `registry:`), not directories
- Directory scans use `dir:path` format
- Image scans use `docker:image:tag` format

---

## 🛠️ Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `403 Forbidden` | Invalid API key or region mismatch | Verify `TMAS_API_KEY` and `VISION_ONE_REGION` match |
| `UnknownArtifactSourceError` | Wrong artifact format | Use `dir:` or `docker:` prefix correctly |
| `InvalidMalwareScanArtifactTypeError` | Used `--malware` on directory | Remove `--malware` from `dir:` scans |
| `API key not found` | Secret not set in GitHub | Add `TMAS_API_KEY` in repo settings |
| Permission denied (Vision One) | Role missing "Run artifact scan" | Update role in User Roles page |

---

## 🎬 Suggested Demo Flow (for SE/Sales)

1. **Show the codebase** — Open `trendai-demo-python/config.py` and highlight visible hardcoded secrets
2. **Push or trigger the workflow** — Demonstrate automated CI/CD integration
3. **Open Actions tab** — Show workflow running in real-time
4. **Expand scan output** — Walk through detected CVEs and secrets
5. **Open Vision One Console** — Show findings centralized across projects
6. **Discuss remediation** — Show fixed versions, suggest override files for false positives

**Recommended demo duration:** ~15 minutes

---

## 📚 Resources

- 📖 [TMAS Official Documentation](https://docs.trendmicro.com/en-us/documentation/article/trend-vision-one-tmas-about)
- 🌐 [TrendAI Vision One Console](https://portal.xdr.trendmicro.com/)
- 📦 [TMAS CLI Downloads](https://ast-cli.xdr.trendmicro.com/tmas-cli/metadata.json)
- 🔧 [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 📄 License & Disclaimer

This repository is for **demonstration and educational purposes only**.

- All API keys, tokens, and credentials are **dummy values**
- "Malware" patterns are **simulated** and non-functional
- Vulnerable code is **intentional** for scanner testing
- **Do not deploy any of these applications** to production environments

---

**Ready to start? → Jump to [Step 1: Get Your API Key](#step-1--get-your-api-key)** 🚀
