from playwright.sync_api import Page
from tests.ui.pages.base_page import BasePage

class HomePage(BasePage):
    SEARCH_INPUT = "[data-testid='search-input']"
    LOCATION_INPUT = "[data-testid='search-location-input']"
    SEARCH_SUBMIT = "[data-testid='search-submit-btn']"
    RESULTS_COUNT = "[data-testid='results-count-heading']"
    JOB_CARDS = "[data-testid^='job-card-']"
    EMPTY_STATE = "[data-testid='empty-search-state']"
    CLEAR_FILTERS_BTN = "[data-testid='clear-filters-btn']"
    FILTER_LOCATION = "[data-testid='filter-location-select']"
    FILTER_JOBTYPE = "[data-testid='filter-jobtype-select']"
    FILTER_EXPERIENCE = "[data-testid='filter-experience-select']"
    FILTER_SALARY = "[data-testid='filter-salary-select']"
    FILTER_SORT = "[data-testid='filter-sort-select']"
    NAV_LOGIN_BTN = "[data-testid='nav-login-btn']"
    NAV_REGISTER_BTN = "[data-testid='nav-register-btn']"
    USER_PROFILE_BADGE = "[data-testid='user-profile-badge']"
    USER_DISPLAY_NAME = "[data-testid='user-display-name']"
    NAV_LOGOUT_BTN = "[data-testid='nav-logout-btn']"
    NAV_CANDIDATE_DASHBOARD = "[data-testid='nav-candidate-dashboard']"
    NAV_RECRUITER_DASHBOARD = "[data-testid='nav-recruiter-dashboard']"

    def search_jobs(self, keyword: str = "", location: str = ""):
        if keyword:
            self.fill(self.SEARCH_INPUT, keyword)
        if location:
            self.fill(self.LOCATION_INPUT, location)
        self.click(self.SEARCH_SUBMIT)
        self.wait_for_timeout(600)  # Wait for API and render

    def filter_by_location(self, location: str):
        self.select_option(self.FILTER_LOCATION, location)
        self.wait_for_timeout(600)

    def filter_by_job_type(self, job_type: str):
        self.select_option(self.FILTER_JOBTYPE, job_type)
        self.wait_for_timeout(600)

    def filter_by_salary(self, salary_val: str):
        self.select_option(self.FILTER_SALARY, salary_val)
        self.wait_for_timeout(600)

    def filter_by_sort(self, sort_val: str):
        self.select_option(self.FILTER_SORT, sort_val)
        self.wait_for_timeout(600)

    def reset_filters(self):
        self.click(self.CLEAR_FILTERS_BTN)
        self.wait_for_timeout(600)

    def get_job_cards_count(self) -> int:
        self.wait_for_timeout(400)
        return self.page.locator(self.JOB_CARDS).count()

    def click_job_details(self, job_id: int):
        self.click(f"[data-testid='job-details-btn-{job_id}']")

    def click_save_job(self, job_id: int):
        self.click(f"[data-testid='job-save-btn-{job_id}']")
        self.wait_for_timeout(400)

    def open_login_modal(self):
        self.click(self.NAV_LOGIN_BTN)

    def open_register_modal(self):
        self.click(self.NAV_REGISTER_BTN)

    def logout(self):
        self.click(self.NAV_LOGOUT_BTN)
        self.wait_for_timeout(400)

    def is_logged_in(self) -> bool:
        return self.is_visible(self.USER_PROFILE_BADGE, timeout=2000)
