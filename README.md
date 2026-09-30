<div align="center">

# 🎯 HireMatch QA — SDET Automation Framework

### Intelligent Job Search & Recruitment Platform Test Suite

[![CI Pipeline](https://github.com/anirudhgup7a/hirematch-sdet-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/anirudhgup7a/hirematch-sdet-automation/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Pytest](https://img.shields.io/badge/tested%20with-pytest-blue.svg)](https://docs.pytest.org)
[![Playwright](https://img.shields.io/badge/UI-Playwright-green.svg)](https://playwright.dev/python/)
[![Locust](https://img.shields.io/badge/perf-Locust-orange.svg)](https://locust.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A production-grade, end-to-end SDET automation project demonstrating API testing, UI automation, database validation, performance testing, and CI/CD pipeline integration — built as a job-portal platform inspired by **Naukri.com / Info Edge**.*

</div>

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Test Coverage](#-test-coverage)
- [Quick Start](#-quick-start)
- [Running Tests](#-running-tests)
- [Project Structure](#-project-structure)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Test Reports](#-test-reports)
- [Key SDET Skills Demonstrated](#-key-sdet-skills-demonstrated)
- [Author](#-author)

---

## 🏗 Project Overview

**HireMatch QA** is a fully functional job search and recruitment platform with:

- **FastAPI Backend** — RESTful API with JWT authentication, role-based access (Candidate/Recruiter), job CRUD, application management, and saved jobs
- **React Frontend** — TypeScript SPA with login/registration, job search/filter, candidate & recruiter dashboards
- **Comprehensive Test Suite** — 66+ automated test cases covering API, UI, database, security, negative, and performance testing

This is **not** a toy project — it's a complete, deployable application with a professional-grade test automation framework built on industry best practices.

---

## 🏛 Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    HireMatch QA Platform                       │
├──────────────┬───────────────┬──────────────┬─────────────────┤
│  React SPA   │  FastAPI REST │   SQLite     │  Test Framework │
│  (Vite+TS)   │  (Uvicorn)   │   Database   │  (Pytest)       │
├──────────────┼───────────────┼──────────────┼─────────────────┤
│ • Auth Modal │ • /auth/*    │ • Users      │ • API Tests     │
│ • Job Search │ • /jobs/*    │ • Jobs       │ • UI Tests      │
│ • Dashboard  │ • /apps/*   │ • Applications│ • DB Tests      │
│ • Job Cards  │ • /saved/*  │ • SavedJobs  │ • Perf Tests    │
│ • Filters    │ • /health   │ • Profiles   │ • Negative Tests│
└──────────────┴───────────────┴──────────────┴─────────────────┘
         │              │              │              │
         └──────────────┴──────────────┴──────────────┘
                    GitHub Actions CI/CD
```

---

## 🛠 Tech Stack

| Layer           | Technology                          | Purpose                    |
|-----------------|-------------------------------------|----------------------------|
| **Backend**     | Python 3.11 + FastAPI + SQLAlchemy  | REST API + ORM             |
| **Frontend**    | React 18 + TypeScript + Vite        | Single Page Application    |
| **Database**    | SQLite (dev) / PostgreSQL (prod)    | Persistent storage         |
| **Auth**        | JWT (python-jose) + bcrypt          | Token-based authentication |
| **API Testing** | Pytest + Requests + HTTPX           | REST endpoint automation   |
| **UI Testing**  | Playwright (Python)                 | Browser E2E automation     |
| **Perf Testing**| Locust                              | Load & stress testing      |
| **Reporting**   | pytest-html                         | HTML test reports           |
| **Logging**     | Custom structured logger            | Test execution traceability|
| **CI/CD**       | GitHub Actions                      | Automated pipeline         |
| **Containers**  | Docker + Docker Compose             | Reproducible environments  |

---

## 📊 Test Coverage

| Category            | Tests | Framework    | Markers                    |
|---------------------|-------|-------------|----------------------------|
| API — Auth          | 10    | Pytest      | `smoke`, `api`, `security` |
| API — Jobs          | 13    | Pytest      | `regression`, `api`        |
| API — Applications  | 7     | Pytest      | `regression`, `api`        |
| API — Saved Jobs    | 4     | Pytest      | `regression`, `api`        |
| API — Negative      | 6     | Pytest      | `negative`, `security`     |
| Database Validation | 12    | Pytest+SQL  | `regression`               |
| UI — Auth Flows     | 4     | Playwright  | `ui`, `smoke`              |
| UI — Job Search     | 3     | Playwright  | `ui`, `regression`         |
| Performance         | 5+    | Locust      | `smoke`, `regression`      |
| **Total**           |**66+**|             |                            |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Git

### 1. Clone & Setup

```bash
git clone https://github.com/anirudhgup7a/hirematch-sdet-automation.git
cd hirematch-sdet-automation

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r backend/requirements.txt
pip install -r requirements-test.txt

# Install Playwright browsers
python -m playwright install chromium
```

### 2. Seed Database & Start Backend

```bash
cd backend
python seed.py
uvicorn app.main:app --reload --port 8000
```

### 3. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Verify Setup

```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs
```

---

## 🧪 Running Tests

### Run All Tests
```bash
pytest tests/ -v --html=reports/test_report.html --self-contained-html
```

### By Category (Markers)
```bash
# Smoke tests (critical path)
pytest -m smoke -v

# API tests only
pytest -m api -v

# UI tests (requires running frontend)
pytest -m ui -v

# Negative / edge case tests
pytest -m negative -v

# Security tests (RBAC, auth bypass)
pytest -m security -v

# Database validation
pytest tests/db/ -v

# Data-driven parametrized tests
pytest -m data_driven -v
```

### Performance Tests (Locust)
```bash
# Headless (CI mode)
locust -f tests/performance/locustfile.py --headless \
  --users 50 --spawn-rate 10 --run-time 120s \
  --host http://localhost:8000 --html reports/perf_report.html

# Interactive (Web UI)
locust -f tests/performance/locustfile.py --host http://localhost:8000
# → Open http://localhost:8089
```

### Docker (Full Stack)
```bash
docker compose up --build

# Run tests in container
docker compose --profile test up
```

---

## 📁 Project Structure

```
hirematch-sdet-automation/
│
├── 📁 backend/                       # FastAPI REST API
│   ├── app/
│   │   ├── main.py                   # App entry point, middleware
│   │   ├── config.py                 # Environment configuration
│   │   ├── database.py               # SQLAlchemy engine setup
│   │   ├── models.py                 # ORM models (User, Job, Application...)
│   │   ├── schemas.py                # Pydantic request/response schemas
│   │   ├── auth.py                   # JWT token creation & validation
│   │   └── routers/
│   │       ├── auth_router.py        # /auth/* endpoints
│   │       ├── jobs_router.py        # /jobs/* endpoints
│   │       ├── applications_router.py# /applications/* endpoints
│   │       └── saved_jobs_router.py  # /saved-jobs/* endpoints
│   ├── seed.py                       # Database seeding script
│   ├── requirements.txt              # Backend Python dependencies
│   └── Dockerfile
│
├── 📁 frontend/                      # React + TypeScript SPA
│   ├── src/
│   │   ├── App.tsx                   # Main application component
│   │   ├── api.ts                    # API client (Axios)
│   │   ├── types.ts                  # TypeScript interfaces
│   │   ├── components/               # UI components
│   │   │   ├── AuthModal.tsx
│   │   │   ├── JobCard.tsx
│   │   │   ├── JobFilters.tsx
│   │   │   ├── JobModal.tsx
│   │   │   ├── Navbar.tsx
│   │   │   ├── PostJobModal.tsx
│   │   │   ├── CandidateDashboard.tsx
│   │   │   └── RecruiterDashboard.tsx
│   │   └── context/
│   │       └── AuthContext.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── 📁 tests/                         # ✨ SDET Automation Suite
│   ├── conftest.py                   # Shared fixtures & hooks
│   ├── pytest.ini                    # Pytest configuration
│   │
│   ├── 📁 api/                       # REST API Test Automation
│   │   ├── api_client.py             # Reusable API client wrapper
│   │   ├── test_auth_api.py          # Auth endpoint tests
│   │   ├── test_jobs_api.py          # Job CRUD tests
│   │   ├── test_applications_api.py  # Application workflow tests
│   │   ├── test_saved_jobs_api.py    # Saved jobs tests
│   │   └── test_negative_api.py      # Negative & security tests
│   │
│   ├── 📁 ui/                        # UI End-to-End Automation
│   │   ├── pages/                    # Page Object Model (POM)
│   │   │   ├── base_page.py          # Base page (shared methods)
│   │   │   ├── home_page.py          # Homepage POM
│   │   │   ├── login_page.py         # Login modal POM
│   │   │   ├── job_details_modal.py  # Job details POM
│   │   │   ├── candidate_dashboard_page.py
│   │   │   └── recruiter_dashboard_page.py
│   │   ├── test_auth_ui.py           # UI auth flow tests
│   │   └── test_job_search_ui.py     # UI search/filter tests
│   │
│   ├── 📁 db/                        # Database Validation
│   │   └── test_database_validation.py # Schema, FK, data integrity
│   │
│   ├── 📁 performance/               # Load & Performance Testing
│   │   └── locustfile.py             # Locust load test scenarios
│   │
│   ├── 📁 test_data/                 # Data-Driven Test Data (JSON)
│   │   ├── auth_scenarios.json
│   │   ├── jobs_data.json
│   │   └── search_scenarios.json
│   │
│   └── 📁 utils/                     # Test Utilities
│       └── logger.py                 # Structured logging utility
│
├── 📁 docs/
│   └── TEST_PLAN.md                  # Master Test Plan & Traceability
│
├── 📁 .github/workflows/
│   └── ci.yml                        # GitHub Actions CI/CD Pipeline
│
├── docker-compose.yml                # Full stack orchestration
├── Dockerfile.test                   # Test runner container
├── requirements-test.txt             # Test Python dependencies
├── .gitignore
└── README.md                         # ← You are here
```

---

## ⚙️ CI/CD Pipeline

The GitHub Actions pipeline runs automatically on every push and PR:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌─────────────┐
│   🔍 Lint   │────▶│  🧪 API     │────▶│  ⚡ Performance │────▶│  📊 Summary │
│  (flake8,   │     │   Tests     │     │   (Locust)       │     │  (Report)   │
│   black)    │     │  (Pytest)   │     │                  │     │             │
└─────────────┘     └──────────────┘     └─────────────────┘     └─────────────┘
                           │
                    ┌──────────────┐
                    │  🎭 UI      │
                    │   Tests     │
                    │ (Playwright)│
                    └──────────────┘
```

### Pipeline Jobs:
1. **Lint** — Code quality (flake8, black, isort)
2. **API Tests** — Smoke → Regression → Negative → DB validation
3. **UI Tests** — Playwright E2E with screenshot-on-failure
4. **Performance** — Locust load test with SLA assertions
5. **Summary** — Aggregate pass/fail report

---

## 📈 Test Reports

After running tests, reports are generated in `reports/`:

| Report                  | Description                        |
|------------------------|------------------------------------|
| `test_report.html`      | Full pytest HTML report            |
| `smoke_report.html`     | Smoke test results                 |
| `api_report.html`       | API test results                   |
| `ui_report.html`        | UI test results with screenshots   |
| `perf_report.html`      | Locust performance dashboard       |
| `perf_stats_stats.csv`  | Performance statistics CSV         |
| `logs/test_run_*.log`   | Structured execution logs          |
| `screenshots/`          | Failure screenshots (Playwright)   |

---

## 🎯 Key SDET Skills Demonstrated

| Skill                     | Implementation                                |
|--------------------------|-----------------------------------------------|
| **Test Automation**       | 66+ automated test cases with Pytest          |
| **REST API Testing**      | Full CRUD coverage with reusable API client   |
| **UI Automation**         | Playwright E2E with Page Object Model (POM)   |
| **Negative Testing**      | SQL injection, XSS, boundary, validation      |
| **Data-Driven Testing**   | JSON parametrized test scenarios              |
| **Database Validation**   | Schema, FK, integrity via SQLAlchemy          |
| **Performance Testing**   | Locust load tests with SLA assertions         |
| **Security Testing**      | JWT, RBAC, auth bypass validation             |
| **CI/CD**                 | GitHub Actions multi-stage pipeline           |
| **Test Reporting**        | HTML reports, screenshots, structured logs    |
| **Docker**                | Multi-service Docker Compose setup            |
| **Clean Architecture**    | Modular POM, fixtures, reusable clients       |
| **Logging**               | Colored console + rotating file logs          |
| **Test Markers**          | Organized by smoke/regression/negative/etc.   |

---

## 👤 Author

**Anirudh Gupta**
- GitHub: [@anirudhgup7a](https://github.com/anirudhgup7a)
- Built as a portfolio project for SDET internship/full-time roles

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
