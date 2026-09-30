import pytest
from tests.api.api_client import HireMatchAPIClient

@pytest.mark.api
@pytest.mark.negative
class TestNegativeAndSecurityAPI:

    def test_sql_injection_attempt_in_search_keyword(self, api_client: HireMatchAPIClient):
        """Verify API safely escapes SQL injection attempts in search queries."""
        sql_injection_payload = "' OR '1'='1' --"
        res = api_client.get_jobs(params={"keyword": sql_injection_payload})
        # Should return 200 with 0 results, never crash or return all rows unfiltered
        assert res.status_code == 200
        assert res.data["total"] == 0

    def test_sql_injection_attempt_in_login(self, api_client: HireMatchAPIClient):
        """Verify API rejects SQL injection payloads in email and password."""
        sql_email = "admin' OR 1=1 --"
        res = api_client.login(sql_email, "somepassword")
        # Pydantic email validation catches invalid email -> 422
        assert res.status_code in [401, 422]

    def test_xss_script_tag_in_cover_letter(self, candidate_client: HireMatchAPIClient):
        """Verify XSS script tags are accepted as plain text and safely stored without execution."""
        xss_string = "<script>alert('xss-vulnerability')</script>"
        res = candidate_client.apply({
            "job_id": 6,
            "cover_letter": xss_string
        })
        assert res.status_code in [201, 409]  # 201 if first time, 409 if already applied
        if res.status_code == 201:
            assert res.data["cover_letter"] == xss_string

    def test_invalid_http_method_on_endpoint(self, api_client: HireMatchAPIClient):
        """Verify calling an unsupported HTTP method returns 405 Method Not Allowed."""
        # /auth/register does not support GET
        res = api_client.request("GET", "/auth/register")
        assert res.status_code == 405

    def test_malformed_json_body(self, api_client: HireMatchAPIClient):
        """Verify sending invalid JSON body returns HTTP 422 Unprocessable Entity."""
        res = api_client.session.post(
            f"{api_client.base_url}/auth/login",
            data="{invalid_json: true,",
            headers={"Content-Type": "application/json"}
        )
        assert res.status_code == 422

    def test_negative_pagination_values(self, api_client: HireMatchAPIClient):
        """Verify negative or zero page values fail validation (HTTP 422)."""
        res = api_client.get_jobs(params={"page": 0, "size": -5})
        assert res.status_code == 422

    def test_excessive_page_size_rejected(self, api_client: HireMatchAPIClient):
        """Verify exceeding max page size limit (100) fails validation (HTTP 422)."""
        res = api_client.get_jobs(params={"size": 500})
        assert res.status_code == 422

    @pytest.mark.smoke
    def test_health_check_system_status(self, api_client: HireMatchAPIClient):
        """Verify API health check endpoint returns 200 OK and database status is UP."""
        res = api_client.health()
        assert res.status_code == 200
        assert res.data["status"] == "UP"
        assert res.data["database"] == "healthy"
        assert "version" in res.data
        assert res.elapsed_ms < 500
