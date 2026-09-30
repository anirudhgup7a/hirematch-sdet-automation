import pytest
from tests.api.api_client import HireMatchAPIClient

@pytest.mark.api
class TestSavedJobsAPI:

    @pytest.mark.smoke
    def test_toggle_save_and_unsave_job(self, candidate_client: HireMatchAPIClient):
        """Verify toggle save API saves on first click and removes on second click."""
        job_id = 4  # Junior QA Analyst

        # 1. First toggle -> Save
        res1 = candidate_client.toggle_saved_job(job_id)
        assert res1.status_code == 200
        assert res1.data["saved"] is True
        assert res1.data["job_id"] == job_id

        # 2. Second toggle -> Unsave
        res2 = candidate_client.toggle_saved_job(job_id)
        assert res2.status_code == 200
        assert res2.data["saved"] is False

    @pytest.mark.regression
    def test_get_saved_jobs_list(self, candidate_client: HireMatchAPIClient):
        """Verify candidate can fetch their saved jobs with embedded job metadata."""
        toggle_res = candidate_client.toggle_saved_job(3)
        if not toggle_res.data or not toggle_res.data.get("saved"):
            candidate_client.toggle_saved_job(3)
        res = candidate_client.get_saved_jobs()
        assert res.status_code == 200
        assert isinstance(res.data, list)
        assert len(res.data) >= 1
        assert "job" in res.data[0]
        assert "title" in res.data[0]["job"]

    @pytest.mark.regression
    def test_unsave_job_endpoint(self, candidate_client: HireMatchAPIClient):
        """Verify DELETE /saved-jobs/{id} explicitly unsaves a job."""
        job_id = 5
        candidate_client.toggle_saved_job(job_id)

        del_res = candidate_client.unsave_job(job_id)
        assert del_res.status_code == 200
        assert f"Job {job_id} unsaved" in del_res.data["message"]

    @pytest.mark.negative
    def test_unsave_non_saved_job_404(self, candidate_client: HireMatchAPIClient):
        """Verify trying to unsave a job that was not bookmarked returns HTTP 404."""
        res = candidate_client.unsave_job(999999)
        assert res.status_code == 404
        assert "not in your saved list" in res.data.get("detail", "").lower()

    @pytest.mark.security
    @pytest.mark.negative
    def test_unauthenticated_cannot_save_job_401(self, api_client: HireMatchAPIClient):
        """Verify unauthenticated user cannot save jobs (HTTP 401)."""
        api_client.clear_token()
        res = api_client.toggle_saved_job(1)
        assert res.status_code == 401

    @pytest.mark.security
    @pytest.mark.negative
    def test_recruiter_cannot_save_jobs_403(self, recruiter_client: HireMatchAPIClient):
        """Verify recruiter account cannot save jobs (candidate role required) (HTTP 403)."""
        res = recruiter_client.toggle_saved_job(1)
        assert res.status_code == 403
