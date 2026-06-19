"""Handler for Humana website"""

from prefect import task
from prefect.cache_policies import NO_CACHE
from payer_website_autofiller.core.utils import (
    get_sync_browser_context,
    get_virtual_display,
)

URL = (
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

    def __init__(self, payload):
        """Init function"""
        self.payload = payload
        self.question_locators = {}

    @task(cache_policy=NO_CACHE)
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

    @task(cache_policy=NO_CACHE)
    def crawl(self):
        """Crawl and autofill website"""
        self.question_locators["practice_description"].wait_for(state="visible")
        self.question_locators["practice_description"].get_by_role(
            "radio",
            name="I (or providers participating under my TIN) accept Medicare,"
            + " but not Medicaid",
        ).check()

        self.question_locators["telehealth_only"].wait_for(state="visible")
        self.question_locators["telehealth_only"].get_by_role(
            "radio", name="No"
        ).check()

        self.question_locators["provider_name"].wait_for(state="visible")
        self.question_locators["provider_name"].get_by_role("textbox").fill(
            TEST_PROVIDER_NAME
        )

        self.question_locators["practice_tin"].wait_for(state="visible")
        self.question_locators["practice_tin"].get_by_role("textbox").fill(
            TEST_PRACTICE_TIN
        )

        self.question_locators["practice_npi"].wait_for(state="visible")
        self.question_locators["practice_npi"].get_by_role("textbox").fill(
            TEST_PRACTICE_NPI
        )

        self.question_locators["provider_npi"].wait_for(state="visible")
        self.question_locators["provider_npi"].get_by_role("textbox").fill(
            TEST_PROVIDER_NPI
        )

        self.question_locators["contact_name"].wait_for(state="visible")
        self.question_locators["contact_name"].get_by_role("textbox").fill(
            TEST_CONTACT_NAME
        )

        self.question_locators["contact_email"].wait_for(state="visible")
        self.question_locators["contact_email"].get_by_role("textbox").fill(
            TEST_CONTACT_EMAIL
        )

        self.question_locators["practice_specific_states"].wait_for(state="visible")
        self.question_locators["practice_specific_states"].get_by_role(
            "radio",
            name="Yes",
        ).check()

        self.question_locators["next_button"].click()
        print("running")

    def handle(self):
        """main process"""
        with get_virtual_display():
            with get_sync_browser_context() as context:
                page = context.new_page()

                page.goto(URL)
                self.initialize_locators(page)
                self.crawl()


if __name__ == "__main__":
    dummy_payload: dict = {}
    Automation(dummy_payload).handle()
