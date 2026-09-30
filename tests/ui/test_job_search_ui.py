import pytest
from playwright.sync_api import Page
from tests.ui.pages.home_page import HomePage

@pytest.mark.ui
class TestJobSearchUI:

    @pytest.mark.smoke
    def test_search_jobs_by_keyword(self, page: Page, base_ui_url: str):
        """Verify search input filters the displayed job cards matching keyword."""
        home = HomePage(page)
        home.navigate(base_ui_url)

        initial_count = home.get_job_cards_count()
        assert initial_count > 0

        home.search_jobs(keyword="SDET")
        assert home.is_visible(HomePage.JOB_CARDS)
        assert home.get_job_cards_count() >= 1

    @pytest.mark.regression
    def test_filter_by_location(self, page: Page, base_ui_url: str):
        """Verify location dropdown filters job cards to selected city."""
        home = HomePage(page)
        home.navigate(base_ui_url)

        home.filter_by_location("Bengaluru")
        assert home.get_job_cards_count() >= 2
        # Check first card location
        first_loc = page.locator("[data-testid^='job-location-']").first.inner_text()
        assert "Bengaluru" in first_loc

    @pytest.mark.regression
    def test_filter_by_job_type_remote(self, page: Page, base_ui_url: str):
        """Verify job type dropdown filters for Remote positions."""
        home = HomePage(page)
        home.navigate(base_ui_url)

        home.filter_by_job_type("Remote")
        assert home.get_job_cards_count() >= 1

    @pytest.mark.regression
    def test_clear_all_filters(self, page: Page, base_ui_url: str):
        """Verify reset filters button restores full job list."""
        home = HomePage(page)
        home.navigate(base_ui_url)

        initial_count = home.get_job_cards_count()
        home.search_jobs(keyword="NonExistentRoleXYZ999")
        assert home.is_visible(HomePage.EMPTY_STATE)

        home.reset_filters()
        assert home.get_job_cards_count() == initial_count

    @pytest.mark.negative
    def test_no_results_empty_state_rendered(self, page: Page, base_ui_url: str):
        """Verify searching for non-matching keyword displays clean empty state UI."""
        home = HomePage(page)
        home.navigate(base_ui_url)

        home.search_jobs(keyword="AstronautRocketMission2099")
        assert home.is_visible(HomePage.EMPTY_STATE)
        empty_text = home.get_text(HomePage.EMPTY_STATE)
        assert "no matching jobs found" in empty_text.lower()
