# BrandShield AI 🛡️
> *Detect impersonation. Protect your brand.*

BrandShield AI is a Digital Risk Protection (DRP) platform built for **HackXLerate 2026 (Challenge 3: Social & App Monitoring)**. It monitors social media and app stores to identify fake profiles, scam pages, and rogue apps imitating legitimate brands.

---

## ✨ Features

- **🛡️ Official Asset Immunity:** Legitimate accounts and apps are cryptographically whitelisted with a **guaranteed 0 risk score (SAFE)**.
- **🔍 Multi-Signal Risk Scoring:** 0–100 risk scoring based on name similarity, bio description match, developer mismatch, and suspicious keywords.
- **🔤 Look-alike & Phishing Detection:**
  - **Unicode Homoglyphs** (e.g., Cyrillic `е` in `Nikе Customer Care`)
  - **Leetspeak Substitutions** (e.g., `1 -> i` in `N1ke Deals`)
  - **Zero False Positives** on benign normal names (e.g., `Nikita Sports Store`).
- **🌐 Real Source Ingestion:** Live metadata scraping for Google Play Store URLs and public social profiles.
- **⚡ 1-Click Demo Seed:** Built-in button to load a complete judge-ready test dataset (Nike + 9 candidate vectors).
- **📊 Executive Reports:** Instant CSV audit export (`/api/export.csv`) for SOC workflows and compliance.

---


## 🛠️ Technology Stack

- **Backend:** Python 3.11, FastAPI
- **Database:** SQLite / PostgreSQL
- **Algorithms:** RapidFuzz, Levenshtein Distance, regular expressions
- **Frontend:** Pure HTML5, Modern CSS
- **Deployment:** Render Blueprint (`render.yaml`)
