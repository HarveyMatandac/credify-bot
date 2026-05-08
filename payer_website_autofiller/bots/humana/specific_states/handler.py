"""Handler for Humana website (Specific state)"""

import json
import time
from prefect.states import Failed
from payer_website_autofiller.core.utils import (
    get_sync_browser,
    get_browser_context,
    get_virtual_display,
)

SAMPLE_INPUT_JSON = "sample_input/test_input.json"

URL = (
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

    def handle(self):
        """main process"""
        try:
            with get_virtual_display():
                with get_sync_browser() as browser:
                    with get_browser_context(browser) as context:
                        page = context.new_page()

                        page.goto(URL)
                        self.initialize_page_1_locators(page)
                        self.crawl()

                        # For visual checking
                        page.wait_for_timeout(30_000)
                        yield

        except Exception as e:
            print(str(e))
