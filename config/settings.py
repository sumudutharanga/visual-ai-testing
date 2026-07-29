from pathlib import Path

# Project root folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Folders
SCREENSHOT_FOLDER = PROJECT_ROOT / "screenshots"
REPORT_FOLDER = PROJECT_ROOT / "reports"
EXPECTED_IMAGE = PROJECT_ROOT / "figma" / "expected" / "upload_modal.png"
CSS_REPORT_FOLDER = Path("reports/css")

# Browser settings
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 832
HEADLESS = False

SCREENSHOT_NAME = "actual.png"