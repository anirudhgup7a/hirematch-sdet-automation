import time
import pytest
from tests.api.api_client import HireMatchAPIClient

@pytest.mark.api
class TestApplicationsAPI:

    @pytest.mark.smoke
    def test_candidate_apply_job_success(self, api_client: HireMatchAPIClient):
        """Test candidate successfully applies to an active job (HTTP 201)."""
        # Register a unique candidate to test clean apply
        unique_email = f"app_tester_{int(time.time()*1000)}@hirematch.com"
        reg_res = api_client.register({
            "email": unique_email,
            "password": "Password123!",
            "full_name": "Application Test Candidate",
            "role": "candidate"
        })
        login_res = api_client.login(unique_email, "Password123!")
        token = login_res.data["access_token"]

        payload = {
            "job_id": 2,  # Senior QA Architect
            "cover_letter": "I have extensive experience building scalable test benches.",
            "resume_url": "https://hirematch.storage/resumes/test_candidate.pdf"
        }
        res = api_client.apply(payload, token=token)
        assert res.status_code == 201
        assert res.data["job_id"] == 2
        assert res.data["status"] == "Applied"
        assert res.data["cover_letter"] == payload["cover_letter"]

    @pytest.mark.negative
    def test_candidate_double_apply_conflict_409(self, api_client: HireMatchAPIClient):
        """Verify applying twice to the same job triggers HTTP 409 Conflict."""
        # Use candidate2 who already applied to job 1 in seed data
        login_res = api_client.login("candidate2@hirematch.com", "Password123!")
        token = login_res.data["access_token"]

        payload = {
            "job_id": 1,  # Already applied in seed data
            "cover_letter": "Duplicate application attempt"
        }
        res = api_client.apply(payload, token=token)
        assert res.status_code == 409
        assert "already applied" in res.data.get("detail", "").lower()

    @pytest.mark.security
    @pytest.mark.negative
    def test_unauthenticated_apply_401(self, api_client: HireMatchAPIClient):
        """Verify unauthenticated user cannot apply for jobs (HTTP 401)."""
        api_client.clear_token()
        res = api_client.apply({"job_id": 1})
        assert res.status_code == 401

    @pytest.mark.security
    @pytest.mark.negative
    def test_recruiter_forbidden_from_applying_403(self, recruiter_client: HireMatchAPIClient):
        """Verify recruiter account cannot submit job applications (HTTP 403)."""
        res = recruiter_client.apply({"job_id": 1})
        assert res.status_code == 403
        assert "candidate role required" in res.data.get("detail", "").lower()

    @pytest.mark.negative
    def test_apply_non_existent_job_404(self, candidate_client: HireMatchAPIClient):
        """Verify applying to non-existent job ID returns HTTP 404."""
        res = candidate_client.apply({"job_id": 999999})
        assert res.status_code == 404

    @pytest.mark.negative
    def test_apply_inactive_job_400(self, recruiter_client: HireMatchAPIClient, candidate_client: HireMatchAPIClient, jobs_test_data):
        """Verify applying to an inactive/closed job returns HTTP 400."""
        # Create and deactivate a job
        job_payload = jobs_test_data["valid_new_job"].copy()
        job_payload["title"] = f"Closed Role {int(time.time()*1000)}"
        c_res = recruiter_client.create_job(job_payload)
        job_id = c_res.data["id"]
        recruiter_client.delete_job(job_id)  # Deactivate

        # Candidate attempts to apply
        res = candidate_client.apply({"job_id": job_id})
        assert res.status_code == 400
        assert "inactive or closed" in res.data.get("detail", "").lower()

    @pytest.mark.regression
    def test_get_my_applications_candidate(self, candidate_client: HireMatchAPIClient):
        """Verify candidate can fetch list of their submitted applications."""
        res = candidate_client.get_my_applications()
        assert res.status_code == 200
        assert isinstance(res.data, list)
        for app in res.data:
            assert "status" in app
            assert "applied_at" in app

    @pytest.mark.regression
    def test_recruiter_view_job_applicants(self, recruiter_client: HireMatchAPIClient):
        """Verify recruiter can list applicants for a job they posted."""
        res = recruiter_client.get_job_applications(job_id=1)
        assert res.status_code == 200
        assert isinstance(res.data, list)
        assert len(res.data) >= 1
        assert res.data[0]["job_id"] == 1

    @pytest.mark.security
    @pytest.mark.negative
    def test_recruiter_cannot_view_other_recruiters_applicants_403(self, api_client: HireMatchAPIClient):
        """Verify recruiter 2 cannot view applications for recruiter 1's job (HTTP 403)."""
        login_res = api_client.login("recruiter2@hirematch.com", "Password123!")
        token = login_res.data["access_token"]
        res = api_client.get_job_applications(job_id=1, token=token)
        assert res.status_code == 403

    @pytest.mark.regression
    def test_recruiter_update_application_status_shortlisted(self, recruiter_client: HireMatchAPIClient):
        """Verify recruiter can advance applicant status to 'Shortlisted'."""
        res = recruiter_client.update_application_status(application_id=1, status="Shortlisted")
        assert res.status_code == 200
        assert res.data["status"] == "Shortlisted"

    @pytest.mark.regression
    def test_recruiter_update_application_status_interview_scheduled(self, recruiter_client: HireMatchAPIClient):
        """Verify recruiter can advance applicant status to 'Interview Scheduled'."""
        res = recruiter_client.update_application_status(application_id=1, status="Interview Scheduled")
        assert res.status_code == 200
        assert res.data["status"] == "Interview Scheduled"

    @pytest.mark.security
    @pytest.mark.negative
    def test_candidate_cannot_update_application_status_403(self, candidate_client: HireMatchAPIClient):
        """Verify candidates cannot tamper with their own or others' application statuses (HTTP 403)."""
        res = candidate_client.update_application_status(application_id=1, status="Offered")
        assert res.status_code == 403

    @pytest.mark.negative
    def test_update_status_invalid_enum_422(self, recruiter_client: HireMatchAPIClient):
        """Verify invalid application status string fails Pydantic validation (HTTP 422)."""
        res = recruiter_client.update_application_status(application_id=1, status="HiredInstantlyWithoutInterview")
        assert res.status_code == 422
