"""Handler for Humana website"""

import json
from dataclasses import dataclass
from prefect import task
from prefect.cache_policies import NO_CACHE
from patchright.sync_api import TimeoutError as PlaywrightTimeoutError
from payer_website_autofiller.core.utils import (
    get_sync_browser_context,
    get_virtual_display,
)
from payer_website_autofiller.core.exceptions.automation_exceptions import (
    NavigationError,
)

URL = "https://fill.dev/not-exist"


@dataclass
class Info:
    """Type annotation for extract info return"""

    first_name: str
    middle_name: str
    last_name: str
    phone_number: str
    street_address_1: str
    street_address_2: str
    city: str
    state: str
    zip_code: str
    country: str


class Automation:
    """Automation class"""

    def __init__(self, payload):
        """Init function"""
        self.payload = payload
        self.question_locators = {}

    @task(cache_policy=NO_CACHE)
    def _access_url(self, page):
        try:
            page.goto(URL, timeout=10000)
        except PlaywrightTimeoutError as e:
            return NavigationError(
                URL,
                "sample_website",
                "_access_url",
            )

    @task
    def _extract_info(self) -> Info:
        basic_info = self.payload["provider_data"]["basic_info"]
        name_dict = basic_info["name"]
        full_address_dict = basic_info["address"]

        return Info(
            first_name=name_dict["first_name"],
            middle_name=name_dict["middle_name"],
            last_name=name_dict["last_name"],
            phone_number=basic_info["contact_info"]["telephone_number"],
            street_address_1=", ".join(
                item for item in list(full_address_dict.values())[:2]
            ),
            street_address_2=full_address_dict.get("street"),
            city=full_address_dict["city"],
            state=full_address_dict["state"],
            zip_code=full_address_dict["zip_code"],
            country=full_address_dict["country"],
        )

    @task(cache_policy=NO_CACHE)
    def _page_1_process(self, page):
        page.click("text=Identity")
        page.get_by_role("link", name="Simple").click()

    @task(cache_policy=NO_CACHE)
    def _page_2_process(self, page):
        """crawling process"""
        info = self._extract_info()
        page.get_by_role("textbox", name="First name").fill(info.first_name)
        page.get_by_role("textbox", name="Middle name").fill(info.middle_name)
        page.get_by_role("textbox", name="Last name").fill(info.last_name)
        page.get_by_role(
            "textbox",
            name="Phone number",
        ).fill(info.phone_number)
        page.locator("input[autocomplete='address-line1']").nth(0).fill(
            info.street_address_1
        )
        page.locator("input[autocomplete='address-line2']").fill(
            info.street_address_2
        )

        page.locator("div.form-group").filter(has_text="City").locator(
            "input"
        ).fill(info.city)

        page.get_by_label("State").select_option(label=info.state.title())

        page.get_by_role("textbox", name="Zip").fill(info.zip_code)

        page.get_by_label("Country").select_option(label=info.country.title())

        page.get_by_role("button", name="Submit").click()

    def handle(self):
        """main process"""

        with get_virtual_display():
            with get_sync_browser_context() as context:
                page = context.new_page()

                self._access_url(page)

                # For visual checking
                page.wait_for_timeout(5_000)


if __name__ == "__main__":
    with open("tests/inputs/template.json", "r", encoding="utf-8") as file:
        dummy_payload = json.load(file)

    Automation(dummy_payload).handle()
