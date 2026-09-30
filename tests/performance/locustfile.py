"""
HireMatch SDET — Locust Performance Test Suite
───────────────────────────────────────────────
Simulates realistic user load against the HireMatch API to
establish performance baselines and detect regressions.

Scenarios:
  1. Anonymous browsing (job search, health check)
  2. Candidate workflow (login → search → view → apply → save)
  3. Recruiter workflow (login → post job → view applications)

Run headless:
  locust -f tests/performance/locustfile.py --headless \
    --users 50 --spawn-rate 10 --run-time 120s \
    --host http://localhost:8000 --html reports/perf_report.html

Author: Anirudh Gupta
"""

import json
import random
import string
from locust import HttpUser, task, between, events, tag

# ─────────────── PERFORMANCE SLAs ───────────────
# These thresholds define our performance contracts
RESPONSE_TIME_SLA_MS = {
    "health_check": 200,
    "job_search": 500,
    "job_detail": 300,
    "auth_login": 800,
    "apply_job": 1000,
    "post_job": 1000,
}


class AnonymousUser(HttpUser):
    """
    Simulates unauthenticated users browsing the platform.
    Weight: 60% of total traffic (highest proportion).
    """
    weight = 6
    wait_time = between(1, 3)

    @tag("smoke", "anonymous")
    @task(5)
    def health_check(self):
        """Verify API health endpoint responds within SLA."""
        with self.client.get("/health", name="GET /health", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Health check failed: {resp.status_code}")
            elif resp.elapsed.total_seconds() * 1000 > RESPONSE_TIME_SLA_MS["health_check"]:
                resp.failure(f"Health check exceeded SLA: {resp.elapsed.total_seconds()*1000:.0f}ms")

    @tag("regression", "search")
    @task(10)
    def search_jobs(self):
        """Search jobs with random keywords — most common user action."""
        keywords = ["python", "java", "react", "devops", "qa", "sdet", "frontend", "backend", "data"]
        keyword = random.choice(keywords)
        with self.client.get(
            f"/api/v1/jobs/?search={keyword}&skip=0&limit=10",
            name="GET /api/v1/jobs/?search=[keyword]",
            catch_response=True
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Job search failed: {resp.status_code}")
            elif resp.elapsed.total_seconds() * 1000 > RESPONSE_TIME_SLA_MS["job_search"]:
                resp.failure(f"Job search exceeded SLA: {resp.elapsed.total_seconds()*1000:.0f}ms")

    @tag("regression", "browse")
    @task(3)
    def list_all_jobs(self):
        """Paginated job listing without filters."""
        page = random.randint(0, 5)
        self.client.get(
            f"/api/v1/jobs/?skip={page * 10}&limit=10",
            name="GET /api/v1/jobs/?paginated"
        )


class CandidateUser(HttpUser):
    """
    Simulates authenticated candidate workflows:
    login → search → view job → apply → save jobs.
    Weight: 30% of traffic.
    """
    weight = 3
    wait_time = between(2, 5)
    token = None

    def on_start(self):
        """Authenticate as candidate before running tasks."""
        resp = self.client.post(
            "/api/v1/auth/login",
            json={"email": "candidate1@hirematch.com", "password": "Password123!"},
            name="POST /api/v1/auth/login [candidate]"
        )
        if resp.status_code == 200:
            self.token = resp.json().get("access_token")
        else:
            self.token = None

    def _headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    @tag("regression", "candidate")
    @task(8)
    def search_and_view(self):
        """Search for jobs and view a specific result."""
        # Search
        resp = self.client.get(
            "/api/v1/jobs/?search=python&limit=5",
            headers=self._headers(),
            name="GET /api/v1/jobs/ [candidate search]"
        )
        if resp.status_code == 200:
            jobs = resp.json()
            if jobs:
                job_id = jobs[0].get("id", 1)
                self.client.get(
                    f"/api/v1/jobs/{job_id}",
                    headers=self._headers(),
                    name="GET /api/v1/jobs/[id]"
                )

    @tag("regression", "candidate")
    @task(3)
    def apply_to_job(self):
        """Apply to a random job (may fail if already applied — expected)."""
        job_id = random.randint(1, 10)
        with self.client.post(
            f"/api/v1/applications/",
            json={"job_id": job_id, "cover_letter": "Locust performance test application"},
            headers=self._headers(),
            name="POST /api/v1/applications/",
            catch_response=True
        ) as resp:
            # 201 = success, 409 = already applied (acceptable)
            if resp.status_code in (201, 409, 400):
                resp.success()
            else:
                resp.failure(f"Apply failed unexpectedly: {resp.status_code}")

    @tag("regression", "candidate")
    @task(2)
    def save_job(self):
        """Save a job to bookmarks."""
        job_id = random.randint(1, 10)
        with self.client.post(
            f"/api/v1/saved-jobs/",
            json={"job_id": job_id},
            headers=self._headers(),
            name="POST /api/v1/saved-jobs/",
            catch_response=True
        ) as resp:
            if resp.status_code in (201, 409, 400, 200):
                resp.success()
            else:
                resp.failure(f"Save job failed: {resp.status_code}")

    @tag("regression", "candidate")
    @task(4)
    def view_my_applications(self):
        """View candidate's own applications."""
        self.client.get(
            "/api/v1/applications/my",
            headers=self._headers(),
            name="GET /api/v1/applications/my"
        )


class RecruiterUser(HttpUser):
    """
    Simulates authenticated recruiter workflows:
    login → post jobs → view applicants.
    Weight: 10% of traffic.
    """
    weight = 1
    wait_time = between(3, 8)
    token = None

    def on_start(self):
        """Authenticate as recruiter."""
        resp = self.client.post(
            "/api/v1/auth/login",
            json={"email": "recruiter1@hirematch.com", "password": "Password123!"},
            name="POST /api/v1/auth/login [recruiter]"
        )
        if resp.status_code == 200:
            self.token = resp.json().get("access_token")
        else:
            self.token = None

    def _headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    @tag("regression", "recruiter")
    @task(5)
    def post_job(self):
        """Post a new job listing as recruiter."""
        rand_suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
        job_data = {
            "title": f"Perf Test Engineer {rand_suffix}",
            "company": "HireMatch QA Corp",
            "location": "Noida, India",
            "job_type": "full-time",
            "experience_level": "mid",
            "salary_min": 800000,
            "salary_max": 1500000,
            "description": f"Performance test job posting {rand_suffix}",
            "requirements": "Python, Locust, Pytest",
            "skills": "python,testing,locust",
        }
        with self.client.post(
            "/api/v1/jobs/",
            json=job_data,
            headers=self._headers(),
            name="POST /api/v1/jobs/ [recruiter]",
            catch_response=True
        ) as resp:
            if resp.status_code in (201, 200):
                resp.success()
            elif resp.status_code == 403:
                resp.failure("Recruiter auth token invalid or expired")
            else:
                resp.failure(f"Post job failed: {resp.status_code}")

    @tag("regression", "recruiter")
    @task(3)
    def view_applications(self):
        """View applications received for recruiter's jobs."""
        self.client.get(
            "/api/v1/applications/",
            headers=self._headers(),
            name="GET /api/v1/applications/ [recruiter]"
        )


# ─────────────── EVENT LISTENERS ───────────────
@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    """Fail the CI run if error rate exceeds 5% or p95 exceeds SLA."""
    stats = environment.runner.stats.total
    fail_ratio = stats.fail_ratio
    p95 = stats.get_response_time_percentile(0.95) or 0

    print("\n" + "=" * 60)
    print("  🏁 Performance Test Summary")
    print("=" * 60)
    print(f"  Total Requests:  {stats.num_requests}")
    print(f"  Failure Rate:    {fail_ratio * 100:.1f}%")
    print(f"  P95 Response:    {p95:.0f}ms")
    print(f"  Avg Response:    {stats.avg_response_time:.0f}ms")
    print(f"  RPS:             {stats.total_rps:.1f}")
    print("=" * 60)

    if fail_ratio > 0.05:
        print("  ❌ FAIL — Error rate exceeded 5% threshold")
        environment.process_exit_code = 1
    elif p95 > 2000:
        print("  ⚠️  WARN — P95 response time exceeded 2000ms")
        environment.process_exit_code = 1
    else:
        print("  ✅ PASS — All performance baselines met")
