# TrendAI Code Security Demo

A demonstration repository with 4 intentionally vulnerable projects for testing **TrendAI Artifact Scanner (TMAS)** integration with GitHub Actions.

**All credentials in this repository are FAKE/DUMMY values for demonstration only.**

---

## 📁 Projects

| Project | Type | Purpose |
|---------|------|---------|
| `trendai-demo-java/` | Spring Boot | Demonstrates CVE detection (Log4Shell) |
| `trendai-demo-python/` | Flask | Demonstrates secrets detection (API keys) |
| `trendai-demo-nodejs/` | Express.js | Demonstrates package vulnerabilities |
| `trendai-demo-docker/` | Docker container | Demonstrates image layer scanning |

---

## 📋 Prerequisites

Before setting up and testing the TMAS scanning workflows, ensure you have:

### 1. TrendMicro Vision One Account
- [ ] Access to [TrendAI Vision One Console](https://portal.xdr.trendmicro.com/)
- [ ] Permissions to create API keys

### 2. TrendAI Vision One API Key
- [ ] Valid API key with **"Run artifact scan"** permission
- [ ] API key associated with your region (e.g., `us-east-1`, `ap-southeast-2`)

**To obtain API key:**
1. Log in to [TrendAI Vision One Console](https://portal.xdr.trendmicro.com/)
2. Navigate to **User Roles** → Create/verify role with "Run artifact scan" permission
3. Go to **API Keys** → Create new key with that role
4. Record the API key and region

### 3. GitHub Repository
- [ ] Fork or clone this repository
- [ ] Admin access to repository settings

### 4. Local Tools (Optional for local testing)
- [ ] Docker (for building container images)
- [ ] TMAS CLI v2.252.0 (for manual scanning)
- [ ] GitHub CLI (`gh`) for manual workflow triggering

---

## 🔧 Step 1: Configure GitHub Secrets

Add your TrendMicro credentials as GitHub secrets so workflows can authenticate with TMAS API.

### Via GitHub Web UI:

1. Go to your repository
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

**Add these secrets:**

| Secret Name | Value | Example |
|-------------|-------|---------|
| `TMAS_API_KEY` | Your Vision One API key | `t1.abcd1234efgh5678...` |
| `VISION_ONE_REGION` | Your region code | `us-east-1` |

**Supported regions:**
- `us-east-1` (default)
- `eu-central-1`
- `ap-southeast-2`
- `ap-southeast-1`
- `ap-northeast-1`
- `ap-south-1`
- `eu-west-2`
- `ca-central-1`
- `me-central-1`

---

## 🚀 Step 2: Run Workflows

Workflows are automatically triggered on push to `main` branch. Or manually trigger them:

### Option A: GitHub Web UI
1. Go to **Actions** tab
2. Select a workflow (e.g., "TMAS Scan — Java")
3. Click **Run workflow**
4. Wait for completion (~2-5 minutes)
5. Check logs for TMAS scan output

### Option B: GitHub CLI
```bash
# Trigger individual workflows
gh workflow run "tmas-scan-java.yml" -R <your-repo> --ref main
gh workflow run "tmas-scan-python.yml" -R <your-repo> --ref main
gh workflow run "tmas-scan-nodejs.yml" -R <your-repo> --ref main
gh workflow run "tmas-scan-docker.yml" -R <your-repo> --ref main

# Or trigger all at once
gh workflow run "tmas-scan-java.yml" -R <your-repo> --ref main && \
gh workflow run "tmas-scan-python.yml" -R <your-repo> --ref main && \
gh workflow run "tmas-scan-nodejs.yml" -R <your-repo> --ref main && \
gh workflow run "tmas-scan-docker.yml" -R <your-repo> --ref main
```

---

## 📖 Step 3: View Results

### Check Workflow Logs

1. Go to **Actions** → Select workflow run
2. Click **debug** job
3. Expand **Run TMAS Scan** step
4. View JSON output with findings

**What to look for:**
- `"vulnerabilities"` section → CVEs found
- `"secrets"` section → Hardcoded credentials detected
- `"malware"` section → Suspicious patterns (Docker image only)

### Workflow Status

All 4 workflows should show **✅ success**:
- `tmas-scan-java.yml` — Directory scan (no malware)
- `tmas-scan-python.yml` — Directory scan (no malware)
- `tmas-scan-nodejs.yml` — Directory scan (no malware)
- `tmas-scan-docker.yml` — 2 jobs: directory + image scan (with malware)

---

## 🏃 Step 4: Local Testing (Optional)

To test TMAS scanning locally without GitHub Actions:

### Install TMAS CLI

```bash
# Download TMAS v2.252.0
curl -L "https://ast-cli.xdr.trendmicro.com/tmas-cli/2.252.0/tmas-cli_Linux_x86_64.tar.gz" | tar xz

# Or for macOS (Intel)
curl -L "https://ast-cli.xdr.trendmicro.com/tmas-cli/latest/tmas-cli_Darwin_x86_64.zip" -o tmas.zip && unzip tmas.zip

# Make executable
chmod +x tmas
```

### Set Environment Variables

```bash
# Set API key and region
export TMAS_API_KEY="your-vision-one-api-key"
export TMAS_REGION="us-east-1"  # or your region

# Verify TMAS version
./tmas --version
```

### Run Scans

**Scan individual projects:**
```bash
# Scan Java project
./tmas scan dir:trendai-demo-java \
  --vulnerabilities --secrets \
  --region $TMAS_REGION

# Scan Python project
./tmas scan dir:trendai-demo-python \
  --vulnerabilities --secrets \
  --region $TMAS_REGION

# Scan Node.js project
./tmas scan dir:trendai-demo-nodejs \
  --vulnerabilities --secrets \
  --region $TMAS_REGION

# Scan Docker source files
./tmas scan dir:trendai-demo-docker \
  --vulnerabilities --secrets \
  --region $TMAS_REGION
```

**Scan Docker image:**
```bash
# Build Docker image
docker build -t trendai-demo-docker:latest ./trendai-demo-docker

# Scan image with malware detection
./tmas scan docker:trendai-demo-docker:latest \
  --vulnerabilities --malware --secrets \
  --region $TMAS_REGION
```

---

## ⚙️ Workflow Files

### What's in `.github/workflows/`

| File | Purpose |
|------|---------|
| `tmas-scan-java.yml` | Scans `trendai-demo-java/` for CVEs and secrets |
| `tmas-scan-python.yml` | Scans `trendai-demo-python/` for CVEs and secrets |
| `tmas-scan-nodejs.yml` | Scans `trendai-demo-nodejs/` for CVEs and secrets |
| `tmas-scan-docker.yml` | Scans Docker source + builds and scans image |

### Workflow Structure

Each workflow:
1. Checks out repository
2. Downloads TMAS CLI v2.252.0
3. Creates `~/.tmas/.env` with API credentials
4. Runs TMAS scan with appropriate flags
5. Reports results (success/failure)

---

## 🔍 Troubleshooting

### Error: "403 Forbidden"
**Cause:** Invalid or mismatched API key/region
- [ ] Verify `TMAS_API_KEY` is correct
- [ ] Verify `VISION_ONE_REGION` matches your API key's region
- [ ] Check API key has "Run artifact scan" permission

### Error: "Unknown artifact type"
**Cause:** Incorrect artifact format in scan command
- [ ] Use `dir:path` for directory scanning
- [ ] Use `docker:image:tag` for container image scanning
- [ ] Never use `artifact:` keyword

### Error: "Malware scanning not supported"
**Cause:** Using `--malware` flag on directory artifact
- [ ] Remove `--malware` for `dir:` scans
- [ ] Only use `--malware` with `docker:`, `registry:`, or image artifacts

### Workflow timeout
**Cause:** Large artifacts or slow network
- [ ] Java builds can take 2-3 minutes
- [ ] Docker image scanning can take 3-5 minutes
- [ ] Check logs for progress

---

## 📝 Next Steps

1. **Setup secrets** (TMAS_API_KEY, VISION_ONE_REGION)
2. **Push to main branch** or manually trigger workflows
3. **Check GitHub Actions** for results
4. **Review scan findings** in workflow logs
5. **Customize** projects for your demo scenario

---

## 🔗 Resources

- [TrendMicro TMAS Documentation](https://docs.trendmicro.com/en-us/documentation/article/trend-vision-one-tmas-about)
- [TrendAI Vision One Console](https://portal.xdr.trendmicro.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## ⚠️ Important Notes

- **All credentials are dummy values** — safe for public repository
- **Workflows require valid TMAS API key** to run
- **Docker image scanning** requires Docker to be available (GitHub-hosted runner has Docker)
- **Malware scanning** only works on container images, not directories

---

**Ready to test? Start with Step 1: Configure GitHub Secrets** ✅
