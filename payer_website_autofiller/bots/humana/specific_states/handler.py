"""Handler for Humana website (Specific state)"""

import json
import time
from contextlib import contextmanager

from patchright.sync_api import sync_playwright
from patchright.sync_api import Error as PlaywrightError

SAMPLE_INPUT_JSON = "sample_input/test_input.json"

TEST_URL = (
    r"https://humana-6853.quickbase.com/nav/app/buwr742wd/action/appoverview/"
    + r"e807d624-39ca-4ddf-aa99-c512a6aa68d5"
)
DATA_AUTOMATION_ID_SELECTOR = 'div[data-automation-id="questionItem"]'


class Automation:
    """Automation class"""

    def __init__(self, payload):
        """Init function"""
        self.payload = payload
        self.question_locators = {}

    def initialize_page_1_locators(self, page):
        """Initialize locators needed"""
        self.question_locators = {}

        self.question_locators["request_to_join_btn"] = page.get_by_role(
            "button"
        ).filter(has_text="Request to Join")
        page.get_by_role("button").filter(has_text="Request to Join").click()

        # page.get_by_test_id("exdb-buttonWidget-createNewRecord").click()

        page.locator(
            'button[data-test-id="exdb-buttonWidget-createNewRecord"]'
        ).click()

    def crawl(self):
        """Crawl and autofill website"""
        pass

    @contextmanager
    def start(self, headless=True):
        """main process"""
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=headless)
            context = browser.new_context()
            page = context.new_page()
            try:
                page.goto(TEST_URL)
                time.sleep(15)
                self.initialize_page_1_locators(page)

                # For visual checking
                page.wait_for_timeout(30_000)
                yield
            except PlaywrightError as e:
                print("Playwright Error: " + str(e))

            except Exception as e:  # pylint: disable=broad-except
                print(str(e))
