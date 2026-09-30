import time
import pytest
from tests.api.api_client import HireMatchAPIClient

@pytest.mark.api
class TestJobsAPI:

    @pytest.mark.smoke
    def test_get_jobs_default_pagination(self, api_client: HireMatchAPIClient):
        """Verify GET /jobs returns paginated list with total count and metadata."""
        res = api_client.get_jobs()
        assert res.status_code == 200
        assert "items" in res.data
        assert "total" in res.data
        assert "page" in res.data
        assert "size" in res.data
        assert res.data["total"] >= 10
        assert len(res.data["items"]) <= 10
        assert res.elapsed_ms < 1000

    @pytest.mark.data_driven
    def test_search_jobs_by_keyword(self, api_client: HireMatchAPIClient, search_test_data):
        """Data-driven test verifying keyword search across title, skills, description."""
        for scenario in search_test_data["keyword_searches"]:
            res = api_client.get_jobs(params={"keyword": scenario["keyword"]})
            assert res.status_code == 200
            assert res.data["total"] >= scenario["expect_min_count"], (
                f"Search for '{scenario['keyword']}' expected >={scenario['expect_min_count']} results, got {res.data['total']}"
            )

    @pytest.mark.data_driven
    def test_filter_jobs_by_location(self, api_client: HireMatchAPIClient, search_test_data):
        """Verify location filtering accurately selects jobs from given city."""
        for filter_item in search_test_data["location_filters"]:
            res = api_client.get_jobs(params={"location": filter_item["location"]})
            assert res.status_code == 200
            assert res.data["total"] >= filter_item["expect_min_count"]
            for job in res.data["items"]:
                assert filter_item["location"].lower() in job["location"].lower()

    @pytest.mark.data_driven
    def test_filter_jobs_by_job_type(self, api_client: HireMatchAPIClient, search_test_data):
        """Verify job_type filter (Full-time, Remote, Hybrid)."""
        for item in search_test_data["job_type_filters"]:
            res = api_client.get_jobs(params={"job_type": item["job_type"]})
            assert res.status_code == 200
            for job in res.data["items"]:
                assert job["job_type"] == item["job_type"]

    @pytest.mark.regression
    def test_filter_jobs_by_min_salary(self, api_client: HireMatchAPIClient):
        """Verify salary filter excludes jobs where max_salary < min_salary filter."""
        min_salary_filter = 1800000  # 18 LPA
        res = api_client.get_jobs(params={"min_salary": min_salary_filter})
        assert res.status_code == 200
        for job in res.data["items"]:
            assert job["max_salary"] >= min_salary_filter

    @pytest.mark.regression
    def test_sort_jobs_by_salary_desc(self, api_client: HireMatchAPIClient):
        """Verify sorting jobs by salary in descending order."""
        res = api_client.get_jobs(params={"sort_by": "salary_desc", "size": 10})
        assert res.status_code == 200
        salaries = [job["max_salary"] for job in res.data["items"]]
        assert salaries == sorted(salaries, reverse=True)

    @pytest.mark.regression
    def test_sort_jobs_by_salary_asc(self, api_client: HireMatchAPIClient):
        """Verify sorting jobs by salary in ascending order."""
        res = api_client.get_jobs(params={"sort_by": "salary_asc", "size": 10})
        assert res.status_code == 200
        salaries = [job["min_salary"] for job in res.data["items"]]
        assert salaries == sorted(salaries)

    @pytest.mark.smoke
    def test_get_search_suggestions(self, api_client: HireMatchAPIClient):
        """Verify search autocomplete suggestions endpoint returns matching strings."""
        res = api_client.get_suggestions(query="SDET")
        assert res.status_code == 200
        assert isinstance(res.data, list)
        assert any("sdet" in s.lower() for s in res.data)

    @pytest.mark.smoke
    def test_get_job_by_id_success(self, api_client: HireMatchAPIClient):
        """Verify retrieving single job by its ID returns full job schema."""
        res = api_client.get_job(1)
        assert res.status_code == 200
        assert res.data["id"] == 1
        assert "title" in res.data
        assert "company_name" in res.data
        assert "requirements" in res.data

    @pytest.mark.negative
    def test_get_job_not_found_404(self, api_client: HireMatchAPIClient):
        """Verify non-existent job ID returns HTTP 404 Not Found."""
        res = api_client.get_job(999999)
        assert res.status_code == 404
        assert "not found" in res.data.get("detail", "").lower()

    @pytest.mark.regression
    def test_recruiter_create_job_success(self, recruiter_client: HireMatchAPIClient, jobs_test_data):
        """Verify recruiter can post a new job opening (HTTP 201)."""
        payload = jobs_test_data["valid_new_job"].copy()
        payload["title"] = f"{payload['title']} - {int(time.time())}"
        res = recruiter_client.create_job(payload)
        assert res.status_code == 201
        assert res.data["title"] == payload["title"]
        assert res.data["is_active"] is True
        assert res.data["recruiter_id"] > 0

    @pytest.mark.security
    @pytest.mark.negative
    def test_candidate_forbidden_from_creating_job_403(self, candidate_client: HireMatchAPIClient, jobs_test_data):
        """Verify candidate role is denied permission to create jobs (HTTP 403)."""
        res = candidate_client.create_job(jobs_test_data["valid_new_job"])
        assert res.status_code == 403
        assert "recruiter role required" in res.data.get("detail", "").lower()

    @pytest.mark.security
    @pytest.mark.negative
    def test_unauthenticated_cannot_create_job_401(self, api_client: HireMatchAPIClient, jobs_test_data):
        """Verify unauthenticated requests cannot post jobs (HTTP 401)."""
        api_client.clear_token()
        res = api_client.create_job(jobs_test_data["valid_new_job"])
        assert res.status_code == 401

    @pytest.mark.regression
    def test_recruiter_update_own_job(self, recruiter_client: HireMatchAPIClient):
        """Verify recruiter can update their own job details."""
        update_data = {
            "title": "Software Development Engineer in Test (SDET) - Automation & Core",
            "min_salary": 1400000,
            "max_salary": 2500000
        }
        res = recruiter_client.update_job(1, update_data)
        assert res.status_code == 200
        assert res.data["title"] == update_data["title"]
        assert res.data["min_salary"] == update_data["min_salary"]

    @pytest.mark.security
    @pytest.mark.negative
    def test_recruiter_cannot_update_another_recruiters_job(self, api_client: HireMatchAPIClient):
        """Verify recruiter cannot modify jobs posted by a different recruiter (HTTP 403)."""
        # Recruiter 2 tries to update Recruiter 1's job (job_id=1)
        login_res = api_client.login("recruiter2@hirematch.com", "Password123!")
        token = login_res.data["access_token"]
        res = api_client.update_job(1, {"title": "Hacked Title"}, token=token)
        assert res.status_code == 403
        assert "do not have permission" in res.data.get("detail", "").lower()

    @pytest.mark.regression
    def test_recruiter_deactivate_job(self, recruiter_client: HireMatchAPIClient, jobs_test_data):
        """Verify recruiter can deactivate an active job posting."""
        # Create a temporary job first
        payload = jobs_test_data["valid_new_job"].copy()
        payload["title"] = f"Job To Deactivate {int(time.time()*1000)}"
        create_res = recruiter_client.create_job(payload)
        job_id = create_res.data["id"]

        del_res = recruiter_client.delete_job(job_id)
        assert del_res.status_code == 200
        assert "inactive" in del_res.data.get("message", "").lower()

        # Check that job is marked is_active = False
        get_res = recruiter_client.get_job(job_id)
        assert get_res.data["is_active"] is False
