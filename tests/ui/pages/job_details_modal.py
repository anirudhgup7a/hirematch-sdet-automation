from playwright.sync_api import Page
from tests.ui.pages.base_page import BasePage

class JobDetailsModal(BasePage):
    MODAL = "[data-testid='job-details-modal']"
    JOB_TITLE = "[data-testid='modal-job-title']"
    JOB_COMPANY = "[data-testid='modal-job-company']"
    JOB_DESCRIPTION = "[data-testid='modal-job-description']"
    COVER_LETTER_INPUT = "[data-testid='application-cover-letter']"
    RESUME_INPUT = "[data-testid='application-resume-input']"
    SUBMIT_APP_BTN = "[data-testid='submit-application-btn']"
    SUCCESS_ALERT = "[data-testid='application-success-alert']"
    ERROR_ALERT = "[data-testid='application-error-alert']"
    LOGIN_TO_APPLY_BTN = "[data-testid='login-to-apply-btn']"
    CLOSE_BTN = "[data-testid='modal-close-btn']"

    def apply(self, cover_letter: str = "", resume_url: str = ""):
        if cover_letter:
            self.fill(self.COVER_LETTER_INPUT, cover_letter)
        if resume_url:
            self.fill(self.RESUME_INPUT, resume_url)
        self.click(self.SUBMIT_APP_BTN)
        self.wait_for_timeout(800)

    def get_success_message(self) -> str:
        return self.get_text(self.SUCCESS_ALERT)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_ALERT)

    def close(self):
        self.click(self.CLOSE_BTN)
        self.wait_for_timeout(300)
