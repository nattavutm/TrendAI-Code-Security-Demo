# TrendAI Code Security Demo

Demo repository สำหรับทดสอบ **TrendAI Artifact Scanner (TMAS)** — สแกนหา CVEs, hardcoded secrets, และ malware patterns อัตโนมัติผ่าน GitHub Actions

> **หมายเหตุ:** Credentials ทั้งหมดในโปรเจกต์นี้เป็น dummy values สำหรับ demo เท่านั้น

---

## โปรเจกต์ที่มีอยู่

| โปรเจกต์ | ภาษา | จุดประสงค์ |
|----------|------|------------|
| `trendai-demo-java/` | Java (Spring Boot) | CVE-2021-44228 (Log4Shell) |
| `trendai-demo-python/` | Python (Flask) | Hardcoded Stripe key, Slack webhook |
| `trendai-demo-nodejs/` | Node.js (Express) | Prototype pollution, insecure deserialization |
| `trendai-demo-docker/` | Docker | Container secrets, malware patterns |

---

## วิธีทดสอบ

### ขั้นตอนที่ 1 — เตรียม API Key

1. ล็อกอิน [TrendAI Vision One Console](https://portal.xdr.trendmicro.com/)
2. ไปที่ **User Roles** → ตรวจสอบว่ามี permission **"Run artifact scan"**
3. ไปที่ **API Keys** → สร้าง API key ใหม่
4. จดบันทึก API key และ region ไว้

---

### ขั้นตอนที่ 2 — ตั้งค่า GitHub Secrets

1. ไปที่ repository → **Settings** → **Secrets and variables** → **Actions**
2. กด **New repository secret** แล้วเพิ่ม 2 ค่า:

| Secret Name | ค่า |
|-------------|-----|
| `TMAS_API_KEY` | API key จากขั้นตอนที่ 1 |
| `VISION_ONE_REGION` | Region เช่น `us-east-1` หรือ `ap-southeast-1` |

---

### ขั้นตอนที่ 3 — รัน Workflow

**วิธีที่ 1: ผ่าน GitHub UI**
1. ไปที่แท็บ **Actions**
2. เลือก workflow ที่ต้องการ เช่น "TMAS Scan — Python"
3. กด **Run workflow**

**วิธีที่ 2: ผ่าน GitHub CLI**
```bash
gh workflow run "tmas-scan-java.yml" --ref main
gh workflow run "tmas-scan-python.yml" --ref main
gh workflow run "tmas-scan-nodejs.yml" --ref main
gh workflow run "tmas-scan-docker.yml" --ref main
```

---

### ขั้นตอนที่ 4 — ดูผลลัพธ์

1. ไปที่แท็บ **Actions** → เลือก workflow run ที่เพิ่งรัน
2. คลิก job → ขยาย step **Run TMAS Scan**
3. ดู JSON output:

```
"vulnerabilities" → CVEs ที่เจอ
"secrets"         → Credentials ที่หลุดอยู่ในโค้ด
"malware"         → Suspicious patterns (เฉพาะ Docker image)
```

---

## การทำงานภายใน

```
push to main
     │
     ▼
GitHub Actions trigger
     │
     ├── ดาวน์โหลด TMAS CLI
     ├── สร้าง ~/.tmas/.env (ใส่ API key + region)
     └── รัน tmas scan
              │
              ├── dir:  → สแกน vulnerabilities + secrets
              └── docker: → สแกน vulnerabilities + secrets + malware
```

---

## Troubleshooting

| Error | สาเหตุ | วิธีแก้ |
|-------|--------|---------|
| `403 Forbidden` | API key ผิด หรือ region ไม่ตรง | ตรวจสอบ `TMAS_API_KEY` และ `VISION_ONE_REGION` |
| `Unknown artifact type` | format ผิด | ใช้ `dir:path` หรือ `docker:image:tag` |
| `Malware not supported` | ใช้ `--malware` กับ directory | เอา `--malware` ออก ใช้กับ docker image เท่านั้น |

---

## Resources

- [TMAS Documentation](https://docs.trendmicro.com/en-us/documentation/article/trend-vision-one-tmas-about)
- [Vision One Console](https://portal.xdr.trendmicro.com/)
