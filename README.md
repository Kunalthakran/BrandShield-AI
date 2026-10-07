# BrandShield AI — Digital Risk Protection Platform
> **HackXLerate 2026 — Challenge 3: "Digital Risk Protection – Social & App Monitoring"**  
> *"Detect impersonation. Protect your brand."*

---

## 🏆 Executive Overview

BrandShield AI is an enterprise-grade Digital Risk Protection (DRP) prototype architected specifically for HackXLerate 2026. The platform monitors external digital surfaces (social media accounts and mobile app marketplaces) to detect impersonation attacks, scam profiles, and rogue applications targeting legitimate brands.

### Key Capabilities Built for Challenge 3:
1. **Protected Brand Identity (Req A):** Define legitimate brand assets (Company name, official website, official social handles, official mobile application, verified developer/publisher, and logo).
2. **Strict Official Asset Exclusion (Req B & C):** Official accounts and applications are cryptographically matched against the brand registry and granted **100% immunity (Risk Score = 0, Status = SAFE)**.
3. **Multi-Signal Risk Scoring Engine (Req B & C):** Deterministic 0–100 risk scoring evaluating:
   - Name Similarity (composite lexical + token match)
   - Description / Bio mimicry
   - Developer / Publisher mismatch
   - Look-alike penalties (homoglyphs & leetspeak)
   - Official whitelist correlation
4. **Look-alike Name Detection Engine (Req D — Bonus Feature):**
   - **Unicode Homoglyph Spoofing:** Identifies cross-alphabet character spoofing (e.g. Cyrillic `е` `U+0435` in `Nikе Customer Care`).
   - **Number Substitution / Leetspeak:** Detects substitutions like `1 -> i` in `N1ke Official Deals`, `0 -> o`, `3 -> e`, `5 -> s`.
   - **Added Impersonation Keywords:** Identifies phishing affixes (`support`, `care`, `rewards`, `official`, `wallet`, `help`).
   - **Benign Name False-Positive Avoidance:** Token-level targeting ensures legitimate normal names (e.g., `Nikita Sports Store`) are **never falsely flagged as impersonators**.
5. **Real Source Ingestion:** Live metadata scraping connectors for Google Play Store app listing URLs and public social media profile pages (no paid API keys required).
6. **SOC Explainability & Remediation:** Every detection explains *WHY* it was flagged with bulleted evidence and recommends actionable SOC workflows (DMCA takedown, app store abuse reporting).
7. **1-Click Demo Seed & CSV Audit Export:** Single-click demo loading for judges (`Nike` brand + 9 multi-vector candidates) and instant CSV incident report downloads.

---

## 🚀 Quick Start (Local Run)

```bash
# 1. Clone repository & navigate to directory
cd BrandShield-AI-Hackathon-Render-Ready

# 2. Set up virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run automated test suite
python smoke_test.py

# 5. Start application
uvicorn main:app --reload --port 8000
```

Open your browser to: **`http://localhost:8000`**

---

## ☁️ 1-Click Render Deployment

This project is 100% **Render-Ready** using `render.yaml` Infrastructure-as-Code Blueprint:

1. Push this folder to a GitHub repository.
2. In the [Render Dashboard](https://dashboard.render.com), click **New + → Blueprint**.
3. Select your repository and click **Apply**.
4. Render will automatically spin up:
   - **Web Service:** Python 3.11 with FastAPI & Uvicorn (`uvicorn main:app --host 0.0.0.0 --port $PORT`).
   - **Database:** Free managed PostgreSQL instance (`brandshield-db`), with automatic `DATABASE_URL` injection.
5. Once deployed, open your Render URL (e.g. `https://brandshield-ai.onrender.com/`).

---

## 🔬 Hackathon Demonstration Walkthrough

When presenting to judges:

1. **Load Pre-configured Demo Data:**
   - In the top header, click **`⚡ Load Demo Data (Nike)`**.
   - Watch the platform automatically seed the official Nike registry and 9 realistic candidate vectors, followed by an immediate multi-signal threat scan.
2. **Review Threat Radar (Tab 1):**
   - Notice the KPI cards: Total Monitored (9), Critical/High Threats (4), Suspicious (1), Protected Assets (3).
   - Inspect the **Verified Official** assets (`@nike`, `@nikeindia`, `Nike (Nike, Inc.)`) — all are scored **0 / SAFE**.
   - Click on **`N1ke Official Deals`** or **`Nikе Customer Care`** to open the **Explainable AI Modal**:
     - See the 0–100 risk score meter.
     - View the decoded Unicode homoglyph (`U+0435 -> 'e'`) or leetspeak substitutions.
     - View the SOC remediation guidance (e.g. DMCA takedown notice).
3. **Interactive Look-alike Lab (Tab 3):**
   - Click Tab 3: **`Look-alike Lab (Req D)`**.
   - Click the preset chips:
     - `N1ke Official Deals` -> Shows Leetspeak substitution `1 -> i`.
     - `Nikе Customer Care` -> Shows Unicode Cyrillic homoglyph `е`.
     - `Nikita Sports Store` -> Demonstrates **Benign Normal Name** protection (similarity capped at 35%, NOT flagged as a look-alike).
4. **Export Compliance Audit Report (Tab 4):**
   - Click Tab 4 or click **`Export CSV`** in the top bar to download `BrandShield_Report_*.csv`.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.11, FastAPI, Pydantic, SQLAlchemy 2.0, Uvicorn
- **Database:** SQLite (local development) / PostgreSQL (production on Render via `psycopg`)
- **Algorithms:** RapidFuzz, Levenshtein Distance, Unicode character decomposition, regular expressions
- **Frontend:** Pure HTML5, Modern CSS (Responsive Light Enterprise Theme), Vanilla JS (Zero node/npm dependencies, zero build step, instant deployment)
- **Deployment:** Render Blueprint (`render.yaml`)
