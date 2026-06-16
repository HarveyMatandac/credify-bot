"""Common utils module"""

import os
import json
import hashlib
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from prefect.client.schemas import FlowRun
from patchright.sync_api import sync_playwright
from pyvirtualdisplay import Display
from prefect.deployments import run_deployment
from payer_website_autofiller.db.crud.job import create_job, get_job
from payer_website_autofiller.core.exceptions import app_exceptions


@contextmanager
def get_virtual_display():
    """PyVirtualDisplay context manager"""
    os.environ["PYVIRTUALDISPLAY_DISPLAYFD"] = "0"
    display = Display(visible=True, backend="xvfb")

    display.start()

    print("display start")
    try:
        yield display
    finally:
        display.stop()
        print("display stopped")


@contextmanager
def get_sync_browser_context():
    """Patchright browser context manager"""

    recording_directory = os.path.join(os.getcwd(), "videos")
    print("recording directory: " + str(recording_directory))
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir=recording_directory)
        try:
            yield context
        finally:
            context.close()
            print("context closed")
            browser.close()
            print("browser closed")


def start_automation(payload, provider_type, db, deployment_name) -> FlowRun:
    """Start job logging and website automation"""
    # Hash request parameters
    job_id = parse_payload(payload)

    flow_run = run_deployment(
        name=deployment_name,
        parameters={
            "payload": payload,
            "provider_type": provider_type,
            "job_id": job_id,
        },
        timeout=0,
    )

    if flow_run is None:
        raise app_exceptions.FlowRunIsNoneError(job_id)

    return flow_run  # type: ignore[return-value]


def parse_payload(payload):
    """Hash payload into sha256 string"""
    json_string = json.dumps(
        payload.model_dump(), sort_keys=True, separators=(",", ":")
    )
    hash_object = hashlib.sha256(json_string.encode("utf-8")).hexdigest()

    return hash_object
