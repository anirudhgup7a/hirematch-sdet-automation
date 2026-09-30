import time
import pytest
from playwright.sync_api import Page
from tests.ui.pages.home_page import HomePage
from tests.ui.pages.login_page import AuthModalPage

@pytest.mark.ui
@pytest.mark.smoke
class TestAuthUI:

    def test_candidate_login_and_logout(self, page: Page, base_ui_url: str):
        """Verify candidate can successfully log in and log out via UI modal."""
        home = HomePage(page)
        auth = AuthModalPage(page)

        home.navigate(base_ui_url)
        assert home.is_visible(HomePage.SEARCH_INPUT)

        home.open_login_modal()
        assert auth.is_visible(AuthModalPage.MODAL)

        auth.login("candidate1@hirematch.com", "Password123!")
        assert home.is_visible(HomePage.USER_PROFILE_BADGE)
        assert "Aarav Patel" in home.get_text(HomePage.USER_DISPLAY_NAME)

        # Logout
        home.logout()
        assert home.is_visible(HomePage.NAV_LOGIN_BTN)

    def test_recruiter_login_shows_recruiter_controls(self, page: Page, base_ui_url: str):
        """Verify recruiter login displays recruiter-specific navigation controls."""
        home = HomePage(page)
        auth = AuthModalPage(page)

        home.navigate(base_ui_url)
        home.open_login_modal()
        auth.login("recruiter1@hirematch.com", "Password123!")

        assert home.is_visible(HomePage.USER_PROFILE_BADGE)
        assert home.is_visible(HomePage.NAV_RECRUITER_DASHBOARD)
        assert "Priya Sharma" in home.get_text(HomePage.USER_DISPLAY_NAME)

    @pytest.mark.negative
    def test_invalid_password_shows_error_message(self, page: Page, base_ui_url: str):
        """Verify entering an incorrect password displays an error notification."""
        home = HomePage(page)
        auth = AuthModalPage(page)

        home.navigate(base_ui_url)
        home.open_login_modal()
        auth.login("candidate1@hirematch.com", "WrongPassword!")

        assert auth.is_visible(AuthModalPage.ERROR_MSG)
        assert "invalid email or password" in auth.get_error_message().lower()

    @pytest.mark.regression
    def test_register_new_candidate_flow(self, page: Page, base_ui_url: str):
        """Verify registering a new candidate creates user session and updates navbar."""
        home = HomePage(page)
        auth = AuthModalPage(page)

        home.navigate(base_ui_url)
        home.open_register_modal()
        assert auth.is_visible(AuthModalPage.MODAL)

        unique_email = f"ui_test_user_{int(time.time()*1000)}@hirematch.com"
        auth.register(
            email=unique_email,
            password="Password123!",
            full_name="UI Automation Candidate",
            role="candidate"
        )

        assert home.is_visible(HomePage.USER_PROFILE_BADGE)
        assert "UI Automation Candidate" in home.get_text(HomePage.USER_DISPLAY_NAME)
