import os
import json
import pytest
from pathlib import Path
from tests.api.api_client import HireMatchAPIClient

ROOT_DIR = Path(__file__).parent.parent
TEST_DATA_DIR = Path(__file__).parent / "test_data"
REPORTS_DIR = ROOT_DIR / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

@pytest.fixture(scope="session")
def base_api_url():
    return os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

@pytest.fixture(scope="session")
def base_ui_url():
    return os.getenv("UI_BASE_URL", "http://localhost:5173")

@pytest.fixture
def api_client(base_api_url):
    return HireMatchAPIClient(base_url=base_api_url)

@pytest.fixture(scope="session")
def auth_test_data():
    with open(TEST_DATA_DIR / "auth_scenarios.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def search_test_data():
    with open(TEST_DATA_DIR / "search_scenarios.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def jobs_test_data():
    with open(TEST_DATA_DIR / "jobs_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def candidate_token(api_client):
    res = api_client.login("candidate1@hirematch.com", "Password123!")
    assert res.status_code == 200, f"Candidate login fixture failed: {res.text}"
    return res.data["access_token"]

@pytest.fixture
def candidate_client(base_api_url, candidate_token):
    client = HireMatchAPIClient(base_url=base_api_url)
    client.set_token(candidate_token)
    return client

@pytest.fixture
def recruiter_token(api_client):
    res = api_client.login("recruiter1@hirematch.com", "Password123!")
    assert res.status_code == 200, f"Recruiter login fixture failed: {res.text}"
    return res.data["access_token"]

@pytest.fixture
def recruiter_client(base_api_url, recruiter_token):
    client = HireMatchAPIClient(base_url=base_api_url)
    client.set_token(recruiter_token)
    return client

# UI Fixtures using Playwright
@pytest.fixture(scope="session")
def playwright_instance():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    yield browser
    browser.close()

@pytest.fixture
def page(browser, request):
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        ignore_https_errors=True
    )
    page = context.new_page()
    yield page

    # Screenshot on test failure
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        test_name = request.node.name.replace("/", "_").replace("::", "_")
        screenshot_path = SCREENSHOTS_DIR / f"{test_name}_failure.png"
        page.screenshot(path=str(screenshot_path), full_page=True)

    page.close()
    context.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
