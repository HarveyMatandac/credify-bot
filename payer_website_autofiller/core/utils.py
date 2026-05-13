"""Common utils module"""

import os
from contextlib import contextmanager
from patchright.sync_api import sync_playwright
from pyvirtualdisplay import Display


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
