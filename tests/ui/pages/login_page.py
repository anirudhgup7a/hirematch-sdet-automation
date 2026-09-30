from playwright.sync_api import Page
from tests.ui.pages.base_page import BasePage

class AuthModalPage(BasePage):
    MODAL = "[data-testid='auth-modal']"
    EMAIL_INPUT = "[data-testid='auth-email-input']"
    PASSWORD_INPUT = "[data-testid='auth-password-input']"
    FULLNAME_INPUT = "[data-testid='auth-fullname-input']"
    ROLE_CANDIDATE = "[data-testid='auth-role-candidate']"
    ROLE_RECRUITER = "[data-testid='auth-role-recruiter']"
    SUBMIT_BTN = "[data-testid='auth-submit-btn']"
    ERROR_MSG = "[data-testid='auth-error-msg']"
    SWITCH_MODE_BTN = "[data-testid='auth-switch-mode-btn']"
    CLOSE_BTN = "[data-testid='auth-modal-close-btn']"

    def login(self, email: str, password: str):
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)
        self.wait_for_timeout(600)

    def register(self, email: str, password: str, full_name: str, role: str = "candidate"):
        if role == "recruiter":
            self.click(self.ROLE_RECRUITER)
        else:
            self.click(self.ROLE_CANDIDATE)
        self.fill(self.FULLNAME_INPUT, full_name)
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)
        self.wait_for_timeout(800)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MSG)

    def switch_mode(self):
        self.click(self.SWITCH_MODE_BTN)
        self.wait_for_timeout(300)

    def close(self):
        self.click(self.CLOSE_BTN)
