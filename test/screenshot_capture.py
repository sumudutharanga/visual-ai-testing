from playwright.sync_api import sync_playwright
import os

from config.settings import (
    VIEWPORT_WIDTH,
    VIEWPORT_HEIGHT,
    HEADLESS,
    SCREENSHOT_FOLDER,
    SCREENSHOT_NAME
)

from data.urls import BASE_URL


def capture_screenshot():

    os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=HEADLESS
        )

        page = browser.new_page(
            viewport={
                "width": VIEWPORT_WIDTH,
                "height": VIEWPORT_HEIGHT
            }
        )

        print("Opening website...")

        page.goto(
            BASE_URL,
            wait_until="networkidle"
        )

        screenshot_path = SCREENSHOT_FOLDER / SCREENSHOT_NAME

        page.screenshot(
            path=screenshot_path,
            full_page=False
        )

        print(f"Screenshot saved : {screenshot_path}")

        browser.close()