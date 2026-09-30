import time
import pytest
from tests.api.api_client import HireMatchAPIClient

@pytest.mark.api
@pytest.mark.smoke
class TestAuthAPI:

    @pytest.mark.data_driven
    def test_valid_login_data_driven(self, api_client: HireMatchAPIClient, auth_test_data):
        """Test valid logins for multiple user roles using data-driven scenarios."""
        for creds in auth_test_data["valid_logins"]:
            res = api_client.login(creds["email"], creds["password"])
            assert res.status_code == 200, f"Expected 200 for {creds['email']}, got {res.status_code}"
            assert "access_token" in res.data
            assert res.data["token_type"] == "bearer"
            assert res.data["user"]["role"] == creds["expected_role"]
            assert res.data["user"]["full_name"] == creds["expected_name"]
            assert res.elapsed_ms < 2000, f"Login took too long: {res.elapsed_ms}ms"

    @pytest.mark.negative
    @pytest.mark.data_driven
    def test_invalid_login_scenarios(self, api_client: HireMatchAPIClient, auth_test_data):
        """Test invalid credentials and input validation on login endpoint."""
        for scenario in auth_test_data["invalid_logins"]:
            res = api_client.login(scenario["email"], scenario["password"])
            assert res.status_code == scenario["expected_status"], (
                f"Scenario '{scenario['scenario']}' expected {scenario['expected_status']} got {res.status_code}"
            )
            if "expected_detail" in scenario and res.status_code == 401:
                assert scenario["expected_detail"] in str(res.data.get("detail", ""))

    @pytest.mark.regression
    def test_register_candidate_success(self, api_client: HireMatchAPIClient):
        """Test creating a fresh candidate user account (HTTP 201)."""
        unique_email = f"auto_cand_{int(time.time()*1000)}@hirematch-test.com"
        payload = {
            "email": unique_email,
            "password": "SecurePassword123!",
            "full_name": "Test Candidate User",
            "role": "candidate"
        }
        res = api_client.register(payload)
        assert res.status_code == 201
        assert res.data["email"] == unique_email.lower()
        assert res.data["role"] == "candidate"
        assert res.data["is_active"] is True
        assert "hashed_password" not in res.data  # Security check: password hash must never leak

    @pytest.mark.regression
    def test_register_recruiter_success(self, api_client: HireMatchAPIClient):
        """Test creating a fresh recruiter user account (HTTP 201)."""
        unique_email = f"auto_rec_{int(time.time()*1000)}@hirematch-test.com"
        payload = {
            "email": unique_email,
            "password": "SecurePassword123!",
            "full_name": "Test Recruiter User",
            "role": "recruiter"
        }
        res = api_client.register(payload)
        assert res.status_code == 201
        assert res.data["email"] == unique_email.lower()
        assert res.data["role"] == "recruiter"

    @pytest.mark.negative
    def test_register_duplicate_email_conflict_409(self, api_client: HireMatchAPIClient):
        """Verify duplicate email registration returns HTTP 409 Conflict."""
        payload = {
            "email": "candidate1@hirematch.com",  # Already exists in seeded data
            "password": "Password123!",
            "full_name": "Duplicate Candidate",
            "role": "candidate"
        }
        res = api_client.register(payload)
        assert res.status_code == 409
        assert "already registered" in res.data.get("detail", "").lower()

    @pytest.mark.negative
    @pytest.mark.data_driven
    def test_register_invalid_payloads(self, api_client: HireMatchAPIClient, auth_test_data):
        """Validate Pydantic validation rejects weak passwords and invalid roles."""
        for item in auth_test_data["invalid_registrations"]:
            payload = {
                "email": item["email"],
                "password": item["password"],
                "full_name": item["full_name"],
                "role": item["role"]
            }
            res = api_client.register(payload)
            assert res.status_code == item["expected_status"], (
                f"Failed for scenario {item['scenario']}: got {res.status_code}"
            )

    @pytest.mark.security
    def test_get_current_user_authenticated(self, candidate_client: HireMatchAPIClient):
        """Verify GET /auth/me returns current user info for authenticated session."""
        res = candidate_client.get_me()
        assert res.status_code == 200
        assert res.data["email"] == "candidate1@hirematch.com"
        assert res.data["role"] == "candidate"

    @pytest.mark.security
    @pytest.mark.negative
    def test_get_current_user_unauthorized_401(self, api_client: HireMatchAPIClient):
        """Verify GET /auth/me returns HTTP 401 Unauthorized without token."""
        api_client.clear_token()
        res = api_client.get_me()
        assert res.status_code == 401

    @pytest.mark.security
    @pytest.mark.negative
    def test_get_current_user_invalid_token_401(self, api_client: HireMatchAPIClient):
        """Verify request with forged/malformed JWT token returns HTTP 401."""
        res = api_client.get_me(token="invalid.bogus.jwt_token_signature")
        assert res.status_code == 401

    @pytest.mark.regression
    def test_candidate_profile_lifecycle(self, candidate_client: HireMatchAPIClient):
        """Verify candidate can fetch and update their profile details."""
        get_res = candidate_client.get_my_profile()
        assert get_res.status_code == 200

        update_payload = {
            "headline": "Lead SDET Automation Specialist",
            "current_company": "Apex Quality Systems",
            "experience_years": 4.5,
            "skills": "Python, Playwright, Pytest, Docker, CI/CD, FastAPI",
            "location": "Bengaluru, Karnataka"
        }
        put_res = candidate_client.update_my_profile(update_payload)
        assert put_res.status_code == 200
        assert put_res.data["headline"] == update_payload["headline"]
        assert put_res.data["experience_years"] == update_payload["experience_years"]
        assert put_res.data["location"] == update_payload["location"]
