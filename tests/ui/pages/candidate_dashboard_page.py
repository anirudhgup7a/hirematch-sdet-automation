from playwright.sync_api import Page
from tests.ui.pages.base_page import BasePage

class CandidateDashboardPage(BasePage):
    DASHBOARD = "[data-testid='candidate-dashboard']"
    TAB_APPLICATIONS = "[data-testid='tab-applications']"
    TAB_SAVED_JOBS = "[data-testid='tab-saved-jobs']"
    APPLICATIONS_TABLE = "[data-testid='applications-table']"
    APPLICATION_ROWS = "[data-testid^='application-row-']"
    COUNT_APPLICATIONS = "[data-testid='count-applications']"
    COUNT_SAVED_JOBS = "[data-testid='count-saved-jobs']"

    def switch_to_applications_tab(self):
        self.click(self.TAB_APPLICATIONS)
        self.wait_for_timeout(400)

    def switch_to_saved_jobs_tab(self):
        self.click(self.TAB_SAVED_JOBS)
        self.wait_for_timeout(400)

    def get_applications_count(self) -> int:
        return self.page.locator(self.APPLICATION_ROWS).count()

    def get_application_status(self, app_id: int) -> str:
        return self.get_text(f"[data-testid='application-status-{app_id}']")
