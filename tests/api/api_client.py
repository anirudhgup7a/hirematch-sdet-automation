import time
import logging
from typing import Any, Dict, Optional
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("HireMatchAPIClient")

class APIResponse:
    def __init__(self, response: requests.Response):
        self.raw_response = response
        self.status_code = response.status_code
        self.headers = response.headers
        self.elapsed_ms = response.elapsed.total_seconds() * 1000.0
        try:
            self.data = response.json()
        except Exception:
            self.data = None
        self.text = response.text

    def __repr__(self):
        return f"<APIResponse status={self.status_code} elapsed={self.elapsed_ms:.1f}ms>"


class HireMatchAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token: Optional[str] = None

    def set_token(self, token: str):
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_token(self):
        self.token = None
        self.session.headers.pop("Authorization", None)

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        token: Optional[str] = None
    ) -> APIResponse:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        req_headers = {}
        if headers:
            req_headers.update(headers)
        if token:
            req_headers["Authorization"] = f"Bearer {token}"
        elif self.token and "Authorization" not in req_headers:
            req_headers["Authorization"] = f"Bearer {self.token}"

        logger.info(f"API Request: {method} {url}")
        t0 = time.time()
        res = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            headers=req_headers
        )
        api_res = APIResponse(res)
        logger.info(f"API Response: {res.status_code} {url} in {api_res.elapsed_ms:.1f}ms")
        return api_res

    # Auth Endpoints
    def register(self, payload: Dict[str, Any]) -> APIResponse:
        return self.request("POST", "/auth/register", json=payload)

    def login(self, email: str, password: str) -> APIResponse:
        return self.request("POST", "/auth/login", json={"email": email, "password": password})

    def get_me(self, token: Optional[str] = None) -> APIResponse:
        return self.request("GET", "/auth/me", token=token)

    def get_my_profile(self, token: Optional[str] = None) -> APIResponse:
        return self.request("GET", "/auth/me/profile", token=token)

    def update_my_profile(self, payload: Dict[str, Any], token: Optional[str] = None) -> APIResponse:
        return self.request("PUT", "/auth/me/profile", json=payload, token=token)

    # Job Endpoints
    def get_jobs(self, params: Optional[Dict[str, Any]] = None) -> APIResponse:
        return self.request("GET", "/jobs", params=params)

    def get_job(self, job_id: int) -> APIResponse:
        return self.request("GET", f"/jobs/{job_id}")

    def get_suggestions(self, query: str) -> APIResponse:
        return self.request("GET", "/jobs/search/suggestions", params={"q": query})

    def create_job(self, payload: Dict[str, Any], token: Optional[str] = None) -> APIResponse:
        return self.request("POST", "/jobs", json=payload, token=token)

    def update_job(self, job_id: int, payload: Dict[str, Any], token: Optional[str] = None) -> APIResponse:
        return self.request("PUT", f"/jobs/{job_id}", json=payload, token=token)

    def delete_job(self, job_id: int, token: Optional[str] = None, hard_delete: bool = False) -> APIResponse:
        return self.request("DELETE", f"/jobs/{job_id}", params={"hard_delete": hard_delete}, token=token)

    def get_recruiter_jobs(self, token: Optional[str] = None) -> APIResponse:
        return self.request("GET", "/jobs/recruiter/my-jobs", token=token)

    # Application Endpoints
    def apply(self, payload: Dict[str, Any], token: Optional[str] = None) -> APIResponse:
        return self.request("POST", "/applications", json=payload, token=token)

    def get_my_applications(self, token: Optional[str] = None) -> APIResponse:
        return self.request("GET", "/applications/my-applications", token=token)

    def get_job_applications(self, job_id: int, token: Optional[str] = None) -> APIResponse:
        return self.request("GET", f"/applications/job/{job_id}", token=token)

    def update_application_status(self, application_id: int, status: str, token: Optional[str] = None) -> APIResponse:
        return self.request("PATCH", f"/applications/{application_id}/status", json={"status": status}, token=token)

    def get_application(self, application_id: int, token: Optional[str] = None) -> APIResponse:
        return self.request("GET", f"/applications/{application_id}", token=token)

    # Saved Jobs Endpoints
    def toggle_saved_job(self, job_id: int, token: Optional[str] = None) -> APIResponse:
        return self.request("POST", "/saved-jobs/toggle", json={"job_id": job_id}, token=token)

    def get_saved_jobs(self, token: Optional[str] = None) -> APIResponse:
        return self.request("GET", "/saved-jobs", token=token)

    def unsave_job(self, job_id: int, token: Optional[str] = None) -> APIResponse:
        return self.request("DELETE", f"/saved-jobs/{job_id}", token=token)

    # Health
    def health(self) -> APIResponse:
        return self.request("GET", "/health")
