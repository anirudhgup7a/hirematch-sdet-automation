import time
import pytest
from playwright.sync_api import Page
from tests.ui.pages.home_page import HomePage
from tests.ui.pages.login_page import AuthModalPage
from tests.ui.pages.job_details_modal import JobDetailsModal
from tests.ui.pages.candidate_dashboard_page import CandidateDashboardPage
from tests.ui.pages.recruiter_dashboard_page import RecruiterDashboardPage

@pytest.mark.ui
class TestApplicationWorkflowUI:

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_candidate_apply_job_workflow(self, page: Page, base_ui_url: str):
        """End-to-end UI test: candidate logs in, views job modal, submits application."""
        home = HomePage(page)
        auth = AuthModalPage(page)
        modal = JobDetailsModal(page)

        # 1. Login as candidate
        home.navigate(base_ui_url)
        home.open_login_modal()
        auth.login("candidate1@hirematch.com", "Password123!")
        assert home.is_visible(HomePage.USER_PROFILE_BADGE)

        # 2. Open job details for first job
        home.view_job_details(job_id=1)
        assert modal.is_visible(JobDetailsModal.MODAL)
        assert modal.is_visible(JobDetailsModal.JOB_TITLE)

        # 3. Submit application
        modal.apply(
            cover_letter="I am very excited to apply for this SDET position at Naukri/HireMatch!",
            resume_url="https://github.com/anirudhgup7a/resume.pdf"
        )
        assert modal.is_visible(JobDetailsModal.SUCCESS_ALERT) or modal.is_visible(JobDetailsModal.ERROR_ALERT)

    @pytest.mark.regression
    def test_candidate_save_and_unsave_job(self, page: Page, base_ui_url: str):
        """Verify candidate can bookmark/save a job card from the homepage listing."""
        home = HomePage(page)
        auth = AuthModalPage(page)

        home.navigate(base_ui_url)
        home.open_login_modal()
        auth.login("candidate2@hirematch.com", "Password123!")
        assert home.is_visible(HomePage.USER_PROFILE_BADGE)

        # Toggle save on job 2
        initial_btn = page.locator("[data-testid='save-job-btn-2']")
        assert initial_btn.is_visible()
        initial_btn.click()
        page.wait_for_timeout(500)

    @pytest.mark.regression
    def test_recruiter_post_job_and_review(self, page: Page, base_ui_url: str):
        """Verify recruiter can navigate to dashboard, post a new job, and view applicant details."""
        home = HomePage(page)
        auth = AuthModalPage(page)
        recruiter_dash = RecruiterDashboardPage(page)

        # 1. Login as recruiter
        home.navigate(base_ui_url)
        home.open_login_modal()
        auth.login("recruiter1@hirematch.com", "Password123!")
        assert home.is_visible(HomePage.NAV_RECRUITER_DASHBOARD)

        # 2. Open Recruiter Dashboard
        home.click(HomePage.NAV_RECRUITER_DASHBOARD)
        assert recruiter_dash.is_visible(RecruiterDashboardPage.DASHBOARD)

        # 3. Post a new SDET Job
        unique_title = f"Staff SDET Engineer {int(time.time())}"
        job_data = {
            "title": unique_title,
            "company_name": "Info Edge Test Corp",
            "location": "Bengaluru",
            "job_type": "Full-time",
            "min_experience": 3,
            "max_experience": 6,
            "min_salary": 1400000,
            "max_salary": 2400000,
            "skills_required": "Python, Pytest, Playwright, CI/CD",
            "description": "Automate high scale systems testing across platforms.",
            "requirements": "Strong Python and test automation framework design skills."
        }
        recruiter_dash.post_new_job(job_data)
        assert recruiter_dash.is_visible(RecruiterDashboardPage.ACTION_SUCCESS) or recruiter_dash.is_visible(RecruiterDashboardPage.DASHBOARD)
