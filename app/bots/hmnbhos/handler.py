"""Handler for Humana website"""

import json
import time
from contextlib import contextmanager
from playwright.sync_api import sync_playwright
from playwright.sync_api import Error as PlaywrightError
from app.dependencies import JobLogger

SAMPLE_INPUT_JSON = "sample_input/test_input.json"

TEST_URL = (
    r"https://forms.office.com/pages/responsepage.aspx?id=vivGVpiFhUue"
    + r"URynU_pQ8hUlKcsMk4ZLvrXNTcI3pF5UMFVFTTVLNjJaSjY2QUNJTzgzUDNFNkgwMy4u"
)
DATA_AUTOMATION_ID_SELECTOR = 'div[data-automation-id="questionItem"]'
TEST_PROVIDER_NAME = "test"
TEST_PRACTICE_TIN = "123456789000"
TEST_PRACTICE_NPI = "1234567893"
TEST_PROVIDER_NPI = "9876543210"
TEST_CONTACT_NAME = "test"
TEST_CONTACT_EMAIL = "contact@sample.com"


class Automation:
    """Automation class"""

    def __init__(self, payload: dict):
        """Init function"""
        self.payload = payload
        self.question_locators = {}

    # @contextmanager
    # def launch_browser(self, headless):
    #     """Launch browser object with automatic handling setup"""
    #     # Create Playwright API object by starting driver process
    #     playwright = sync_playwright().start()
    #     browser = playwright.firefox.launch(headless=headless)
    #     context = browser.new_context()
    #     page = context.new_page()
    #     try:
    #         yield page
    #     finally:
    #         browser.close()
    #         playwright.stop()

    def initialize_locators(self, page):
        """Initialize locators needed"""
        self.question_locators = {}

        self.question_locators["practice_description"] = page.locator(
            DATA_AUTOMATION_ID_SELECTOR
        ).filter(
            has_text="Choose the option below that best describes your "
            + "practice."
        )

        self.question_locators["telehealth_only"] = page.locator(
            DATA_AUTOMATION_ID_SELECTOR
        ).filter(has_text="Are your services via Telehealth only?")

        self.question_locators["provider_name"] = page.locator(
            DATA_AUTOMATION_ID_SELECTOR
        ).filter(has_text="Enter the provider's name")

        self.question_locators["practice_tin"] = page.locator(
            DATA_AUTOMATION_ID_SELECTOR
        ).filter(has_text="Enter your practice TIN")

        self.question_locators["practice_npi"] = page.locator(
            DATA_AUTOMATION_ID_SELECTOR
        ).filter(has_text="Enter your practice NPI")

        self.question_locators["provider_npi"] = page.locator(
            DATA_AUTOMATION_ID_SELECTOR
        ).filter(has_text="Enter your provider NPI")

        self.question_locators["contact_name"] = page.locator(
            DATA_AUTOMATION_ID_SELECTOR
        ).filter(has_text="Enter a contact name")

        self.question_locators["contact_email"] = page.locator(
            DATA_AUTOMATION_ID_SELECTOR
        ).filter(has_text="Enter the contact email")

        self.question_locators["practice_specific_states"] = page.locator(
            DATA_AUTOMATION_ID_SELECTOR
        ).filter(
            has_text="Do you/your practice see patients in any of the "
            + "following states?"
        )
        self.question_locators["next_button"] = page.get_by_role(
            "button", name="Next"
        )

    def crawl(self):
        """Crawl and autofill website"""
        self.question_locators["practice_description"].get_by_role(
            "radio",
            name="I (or providers participating under my TIN) accept Medicare,"
            + " but not Medicaid",
        ).check()
        time.sleep(5)
        self.question_locators["telehealth_only"].get_by_role(
            "radio", name="No"
        ).check()
        time.sleep(5)
        self.question_locators["provider_name"].get_by_role("textbox").fill(
            TEST_PROVIDER_NAME
        )
        time.sleep(5)
        self.question_locators["practice_tin"].get_by_role("textbox").fill(
            TEST_PRACTICE_TIN
        )
        time.sleep(5)
        self.question_locators["practice_npi"].get_by_role("textbox").fill(
            TEST_PRACTICE_NPI
        )
        time.sleep(5)
        self.question_locators["provider_npi"].get_by_role("textbox").fill(
            TEST_PROVIDER_NPI
        )
        time.sleep(5)
        self.question_locators["contact_name"].get_by_role("textbox").fill(
            TEST_CONTACT_NAME
        )
        time.sleep(5)
        self.question_locators["contact_email"].get_by_role("textbox").fill(
            TEST_CONTACT_EMAIL
        )
        time.sleep(5)
        self.question_locators["practice_specific_states"].get_by_role(
            "radio",
            name="Yes",
        ).check()
        time.sleep(5)
        self.question_locators["next_button"].click()

    @contextmanager
    def start(self, headless=True):
        """main process"""
        with sync_playwright() as playwright:
            browser = playwright.firefox.launch(headless=headless)
            context = browser.new_context()
            page = context.new_page()
            try:
                page.goto(TEST_URL)
                self.initialize_locators(page)
                self.crawl()

                # For visual checking
                page.wait_for_timeout(30_000)
                yield
            except PlaywrightError as e:
                print("Playwright Error: " + str(e))

            except Exception as e:  # pylint: disable=broad-except
                print(str(e))


if __name__ == "__main__":
    with open(SAMPLE_INPUT_JSON, "r") as file:
        data_dict = json.load(file)

    Automation(data_dict).start(False)
