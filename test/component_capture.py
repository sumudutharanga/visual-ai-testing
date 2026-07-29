from pathlib import Path
from playwright.sync_api import sync_playwright
from utils.layout_reader import save_layout
from utils.image_cropper import crop_component
from utils.dom_reader import save_dom_info

from config.settings import (
    VIEWPORT_WIDTH,
    VIEWPORT_HEIGHT,
    SCREENSHOT_FOLDER,
    HEADLESS
)
from utils.css_reader import (
    get_css_properties,
    save_css_report
)
from data.urls import BASE_URL

from utils.locators import (
    TITLE,
    DROPZONE,
    IMPORT_BUTTON,
    CANCEL_BUTTON,
    HELP_BUTTON,
    CLOSE_BUTTON,
    URL_INPUT,
    URL_UPLOAD_BUTTON,
    CHOOSE_FILE,
    MODAL
)


# Folder to save component screenshots
COMPONENT_FOLDER = SCREENSHOT_FOLDER/"components"
COMPONENT_FOLDER.mkdir(parents=True, exist_ok=True)


# Components to capture
COMPONENTS = {
    "modal": MODAL,
    "title": TITLE,
    "dropzone": DROPZONE,
    "choose_file": CHOOSE_FILE,
    "url_input": URL_INPUT,
    "url_upload_button": URL_UPLOAD_BUTTON,
    "help_button": HELP_BUTTON,
    "cancel_button": CANCEL_BUTTON,
    "import_button": IMPORT_BUTTON,
    "close_button": CLOSE_BUTTON,
}


def capture_components():

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

        print("\nOpening website...")

        page.goto(
            BASE_URL,
            wait_until="networkidle"
        )

        print("\nCapturing UI Components...\n")

        for name, testid in COMPONENTS.items():

            try:

                element = page.get_by_test_id(testid)

                element.wait_for(state="visible", timeout=5000)
                box = element.bounding_box()
                crop_component(name, box)
                save_layout(name, box)
                css = get_css_properties(page, testid)
                dom_info = {
                    "component": name,
                    "testid": testid,
                    "exists": True,
                    "visible": element.is_visible(),
                    "enabled": element.is_enabled(),
                    "text": element.inner_text().strip(),
                    "tag": element.evaluate("el => el.tagName")
                }

                save_dom_info(name, dom_info)

                save_css_report(name, css)

                save_path = COMPONENT_FOLDER / f"{name}.png"

                element.screenshot(
                    path=str(save_path)
                )

                print(f"✓ {name} saved")
                print(f"\n{name.upper()}")

                print(f"Screenshot : OK")

                print(f"Font Size : {css['fontSize']}")

                print(f"Font Weight : {css['fontWeight']}")

                print(f"Font Family : {css['fontFamily']}")

                print(f"Width : {css['width']}")

                print(f"Height : {css['height']}")

                print(f"Border Radius : {css['borderRadius']}")

                print(f"Background : {css['backgroundColor']}")

                print(f"Text Color : {css['color']}")

            except Exception as e:

                print(f"✗ {name} failed")
                print(e)

        browser.close()

        print("\nComponent capture completed.")