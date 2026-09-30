from typing import Dict, Any
from playwright.sync_api import Page
from tests.ui.pages.base_page import BasePage

class RecruiterDashboardPage(BasePage):
    DASHBOARD = "[data-testid='recruiter-dashboard']"
    POST_JOB_BTN = "[data-testid='recruiter-post-job-btn']"
    APPLICANTS_PANEL = "[data-testid='recruiter-applicants-panel']"
    APPLICANTS_BADGE = "[data-testid='applicants-count-badge']"
    ACTION_SUCCESS = "[data-testid='recruiter-action-success']"

    # Post Job Modal Selectors
    POST_MODAL = "[data-testid='post-job-modal']"
    POST_TITLE = "[data-testid='post-job-title']"
    POST_COMPANY = "[data-testid='post-job-company']"
    POST_LOCATION = "[data-testid='post-job-location']"
    POST_TYPE = "[data-testid='post-job-type']"
    POST_MIN_EXP = "[data-testid='post-job-minexp']"
    POST_MAX_EXP = "[data-testid='post-job-maxexp']"
    POST_MIN_SAL = "[data-testid='post-job-minsalary']"
    POST_MAX_SAL = "[data-testid='post-job-maxsalary']"
    POST_SKILLS = "[data-testid='post-job-skills']"
    POST_DESC = "[data-testid='post-job-description']"
    POST_REQ = "[data-testid='post-job-requirements']"
    POST_SUBMIT = "[data-testid='post-job-submit-btn']"

    def select_job(self, job_id: int):
        self.click(f"[data-testid='recruiter-job-item-{job_id}']")
        self.wait_for_timeout(500)

    def update_applicant_status(self, app_id: int, new_status: str):
        self.select_option(f"[data-testid='status-select-{app_id}']", new_status)
        self.click(f"[data-testid='update-status-btn-{app_id}']")
        self.wait_for_timeout(600)

    def post_new_job(self, job_data: Dict[str, Any]):
        self.click(self.POST_JOB_BTN)
        self.wait_for_timeout(300)
        self.fill(self.POST_TITLE, job_data["title"])
        self.fill(self.POST_COMPANY, job_data["company_name"])
        self.select_option(self.POST_LOCATION, job_data.get("location", "Bengaluru"))
        self.select_option(self.POST_TYPE, job_data.get("job_type", "Full-time"))
        self.fill(self.POST_MIN_EXP, str(job_data.get("min_experience", 2)))
        self.fill(self.POST_MAX_EXP, str(job_data.get("max_experience", 5)))
        self.fill(self.POST_MIN_SAL, str(job_data.get("min_salary", 1000000)))
        self.fill(self.POST_MAX_SAL, str(job_data.get("max_salary", 1800000)))
        self.fill(self.POST_SKILLS, job_data.get("skills_required", "Python, SDET"))
        self.fill(self.POST_DESC, job_data.get("description", "Job description text"))
        self.fill(self.POST_REQ, job_data.get("requirements", "Job requirements text"))
        self.click(self.POST_SUBMIT)
        self.wait_for_timeout(800)
