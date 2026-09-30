from playwright.sync_api import Page, Locator

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, wait_until="networkidle")

    def click(self, selector: str, timeout: int = 5000):
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.click(selector)

    def fill(self, selector: str, text: str, timeout: int = 5000):
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.fill(selector, text)

    def select_option(self, selector: str, value: str, timeout: int = 5000):
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.select_option(selector, value)

    def get_text(self, selector: str, timeout: int = 5000) -> str:
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        return self.page.locator(selector).inner_text().strip()

    def is_visible(self, selector: str, timeout: int = 3000) -> bool:
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def wait_for_timeout(self, ms: int):
        self.page.wait_for_timeout(ms)

    def screenshot(self, path: str):
        self.page.screenshot(path=path, full_page=True)
