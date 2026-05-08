"""Common utils module"""

from contextlib import contextmanager
from patchright.sync_api import sync_playwright
from pyvirtualdisplay import Display


@contextmanager
def get_virtual_display():
    """PyVirtualDisplay context manager"""
    display = Display(visible=True, backend="xvfb")
    display.start()
    try:
        yield display
    finally:
        display.stop()
        print("display stopped")


@contextmanager
def get_sync_browser():
    """Patchright browser context manager"""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        yield browser


@contextmanager
def get_browser_context(browser):
    """Get context from Patchright browser"""
    context = browser.new_context(record_video_dir="/videos")
    try:
        yield context
    finally:
        context.close()
        print("context closed")
