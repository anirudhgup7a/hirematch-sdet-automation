# 📋 HireMatch QA — Master Test Plan

## 1. Project Overview

**HireMatch** is an intelligent job search and recruitment platform (inspired by Naukri.com). This document defines the complete test strategy, test case inventory, and traceability matrix for the SDET automation suite.

| Attribute         | Detail                                  |
|-------------------|-----------------------------------------|
| **Application**   | HireMatch QA Platform                   |
| **Version**       | 1.0.0                                   |
| **Author**        | Anirudh Gupta                           |
| **Test Framework**| Pytest + Playwright + Locust            |
| **Backend**       | FastAPI + SQLAlchemy + SQLite           |
| **Frontend**      | React + TypeScript + Vite               |
| **CI/CD**         | GitHub Actions                          |

---

## 2. Test Strategy

### 2.1 Test Levels

| Level               | Scope                               | Tool         |
|---------------------|--------------------------------------|-------------|
| Unit / Schema       | DB schema, model validation          | Pytest + SQLAlchemy |
| API Integration     | REST endpoints, auth, CRUD           | Pytest + Requests/HTTPX |
| UI End-to-End       | Full browser workflows               | Playwright  |
| Performance         | Load, stress, response time SLAs     | Locust      |
| Security            | Auth bypass, role enforcement, tokens | Pytest      |

### 2.2 Test Types

- ✅ **Smoke Tests** — Critical path sanity (login, health, job search)
- ✅ **Regression Tests** — Full functional coverage
- ✅ **Negative Tests** — Invalid inputs, boundary conditions, error handling
- ✅ **Data-Driven Tests** — Parametrized from JSON test data
- ✅ **Security Tests** — RBAC, token validation, unauthorized access
- ✅ **Database Validation** — Schema, FK, data integrity
- ✅ **Performance Tests** — Load testing with SLA assertions

---

## 3. Test Case Inventory

### 3.1 API Tests — Authentication (`test_auth_api.py`)

| TC-ID    | Test Case                                    | Type     | Priority |
|----------|----------------------------------------------|----------|----------|
| AUTH-001 | Register new candidate successfully          | Smoke    | P0       |
| AUTH-002 | Register new recruiter successfully          | Smoke    | P0       |
| AUTH-003 | Login with valid credentials                 | Smoke    | P0       |
| AUTH-004 | Login with wrong password returns 401        | Negative | P0       |
| AUTH-005 | Login with non-existent email returns 401    | Negative | P1       |
| AUTH-006 | Register with duplicate email returns 400    | Negative | P0       |
| AUTH-007 | Register with missing fields returns 422     | Negative | P1       |
| AUTH-008 | Access protected endpoint without token      | Security | P0       |
| AUTH-009 | Access with expired/invalid JWT              | Security | P0       |
| AUTH-010 | Get current user profile (/auth/me)          | Regression| P1      |

### 3.2 API Tests — Jobs (`test_jobs_api.py`)

| TC-ID    | Test Case                                    | Type     | Priority |
|----------|----------------------------------------------|----------|----------|
| JOB-001  | Recruiter creates a new job listing          | Smoke    | P0       |
| JOB-002  | Search jobs by keyword                       | Smoke    | P0       |
| JOB-003  | Filter jobs by location                      | Regression| P1      |
| JOB-004  | Filter jobs by job_type                      | Regression| P1      |
| JOB-005  | Filter jobs by experience_level              | Regression| P1      |
| JOB-006  | Get specific job by ID                       | Regression| P1      |
| JOB-007  | Update job listing (recruiter)               | Regression| P1      |
| JOB-008  | Delete job listing (recruiter)               | Regression| P2      |
| JOB-009  | Candidate cannot post a job (403)            | Security | P0       |
| JOB-010  | Pagination with skip/limit                   | Regression| P1      |
| JOB-011  | Get non-existent job returns 404             | Negative | P1       |
| JOB-012  | Post job with missing required fields (422)  | Negative | P1       |
| JOB-013  | Salary range validation (min > max)          | Negative | P2       |

### 3.3 API Tests — Applications (`test_applications_api.py`)

| TC-ID    | Test Case                                    | Type     | Priority |
|----------|----------------------------------------------|----------|----------|
| APP-001  | Candidate applies to a job                   | Smoke    | P0       |
| APP-002  | Candidate views own applications             | Regression| P1      |
| APP-003  | Duplicate application returns conflict       | Negative | P0       |
| APP-004  | Recruiter views applicants for their job     | Regression| P1      |
| APP-005  | Recruiter updates application status         | Regression| P1      |
| APP-006  | Candidate cannot update application status   | Security | P0       |
| APP-007  | Apply to non-existent job (404)              | Negative | P1       |

### 3.4 API Tests — Saved Jobs (`test_saved_jobs_api.py`)

| TC-ID    | Test Case                                    | Type     | Priority |
|----------|----------------------------------------------|----------|----------|
| SAV-001  | Candidate saves a job                        | Smoke    | P1       |
| SAV-002  | Candidate views saved jobs list              | Regression| P1      |
| SAV-003  | Candidate unsaves a job                      | Regression| P2      |
| SAV-004  | Duplicate save returns conflict              | Negative | P1       |

### 3.5 API Tests — Negative (`test_negative_api.py`)

| TC-ID    | Test Case                                    | Type     | Priority |
|----------|----------------------------------------------|----------|----------|
| NEG-001  | SQL injection in search parameter            | Security | P0       |
| NEG-002  | XSS payload in job title                     | Security | P0       |
| NEG-003  | Extremely long string input                  | Negative | P1       |
| NEG-004  | Special characters in all text fields        | Negative | P1       |
| NEG-005  | Empty body POST requests                     | Negative | P1       |
| NEG-006  | Wrong HTTP method returns 405                | Negative | P2       |

### 3.6 Database Validation (`test_database_validation.py`)

| TC-ID    | Test Case                                    | Type     | Priority |
|----------|----------------------------------------------|----------|----------|
| DB-001   | All ORM tables exist in database             | Regression| P0      |
| DB-002   | Users table column schema validation         | Regression| P1      |
| DB-003   | Jobs table column schema validation          | Regression| P1      |
| DB-004   | Email unique constraint verified             | Regression| P0      |
| DB-005   | Application composite unique constraint      | Regression| P0      |
| DB-006   | FK: jobs.recruiter_id → users.id             | Regression| P0      |
| DB-007   | FK: applications.job_id → jobs.id            | Regression| P0      |
| DB-008   | No orphaned applications                     | Regression| P1      |
| DB-009   | All user roles are valid                     | Regression| P1      |
| DB-010   | Salary range consistency (min ≤ max)         | Regression| P1      |
| DB-011   | No null emails in users                      | Negative | P0       |
| DB-012   | No future created_at timestamps              | Regression| P2      |

### 3.7 UI Tests — Authentication (`test_auth_ui.py`)

| TC-ID    | Test Case                                    | Type     | Priority |
|----------|----------------------------------------------|----------|----------|
| UI-001   | Login modal opens on button click            | Smoke    | P0       |
| UI-002   | Successful login redirects to dashboard      | Smoke    | P0       |
| UI-003   | Login with wrong password shows error        | Negative | P0       |
| UI-004   | Registration form validation                 | Regression| P1      |

### 3.8 UI Tests — Job Search (`test_job_search_ui.py`)

| TC-ID    | Test Case                                    | Type     | Priority |
|----------|----------------------------------------------|----------|----------|
| UI-005   | Homepage loads with job listings             | Smoke    | P0       |
| UI-006   | Search box filters jobs by keyword           | Regression| P1      |
| UI-007   | Job card click opens detail modal            | Regression| P1      |

### 3.9 Performance Tests (`locustfile.py`)

| TC-ID    | Test Case                                    | Type        | Priority |
|----------|----------------------------------------------|-------------|----------|
| PERF-001 | Health endpoint < 200ms under load           | Performance | P1       |
| PERF-002 | Job search < 500ms under load                | Performance | P1       |
| PERF-003 | Auth login < 800ms under load                | Performance | P1       |
| PERF-004 | Overall error rate < 5%                      | Performance | P0       |
| PERF-005 | P95 response time < 2000ms                   | Performance | P0       |

---

## 4. Traceability Matrix

| Feature Area    | API Tests | UI Tests | DB Tests | Perf Tests | Total |
|-----------------|-----------|----------|----------|------------|-------|
| Authentication  | 10        | 4        | 2        | 1          | **17**|
| Job Management  | 13        | 3        | 3        | 2          | **21**|
| Applications    | 7         | —        | 3        | 1          | **11**|
| Saved Jobs      | 4         | —        | 1        | 1          | **6** |
| Negative/Security| 6        | 1        | 3        | 1          | **11**|
| **Total**       | **40**    | **8**    | **12**   | **6**      | **66**|

---

## 5. Test Environment

| Component    | Technology        | Purpose           |
|-------------|-------------------|-------------------|
| Backend     | FastAPI + SQLite  | API under test    |
| Frontend    | React + Vite      | UI under test     |
| API Testing | Pytest + Requests | REST automation   |
| UI Testing  | Playwright        | Browser automation|
| Perf Testing| Locust            | Load testing      |
| CI/CD       | GitHub Actions    | Pipeline automation|
| Containers  | Docker Compose    | Reproducible env  |

---

## 6. Entry / Exit Criteria

### Entry Criteria
- All dependencies installed (`pip install`, `npm ci`, `playwright install`)
- Database seeded (`python backend/seed.py`)
- API server running (`uvicorn`)
- Frontend built and served

### Exit Criteria
- All P0 smoke tests pass
- Regression suite pass rate ≥ 95%
- No critical/blocker bugs open
- Performance SLAs met under load
- Test report generated and archived

---

## 7. Risk Analysis

| Risk                              | Mitigation                              |
|-----------------------------------|-----------------------------------------|
| Flaky UI tests                    | Explicit waits, retry logic             |
| Database state pollution          | Session rollback, test isolation         |
| Performance baseline drift        | SLA thresholds in Locust assertions     |
| Token expiration during long runs | Fresh auth fixtures per test            |
| CI environment differences        | Docker Compose for consistency          |
