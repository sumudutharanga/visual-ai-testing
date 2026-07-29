from pathlib import Path
import cv2
from skimage.metrics import structural_similarity as ssim

# ======================================================
# Project Paths
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_IMAGE = PROJECT_ROOT / "figma" / "expected" / "upload_modal.png"
ACTUAL_IMAGE = PROJECT_ROOT / "screenshots" / "actual.png"

REPORT_FOLDER = PROJECT_ROOT / "reports"
REPORT_FOLDER.mkdir(exist_ok=True)

DIFFERENCE_IMAGE = REPORT_FOLDER / "difference.png"
HIGHLIGHTED_IMAGE = REPORT_FOLDER / "highlighted.png"
MASK_IMAGE = REPORT_FOLDER / "mask.png"


def compare_images():

    print("Loading images...")

    expected = cv2.imread(str(EXPECTED_IMAGE))
    actual = cv2.imread(str(ACTUAL_IMAGE))

    if expected is None:
        raise FileNotFoundError(f"Expected image not found:\n{EXPECTED_IMAGE}")

    if actual is None:
        raise FileNotFoundError(f"Actual image not found:\n{ACTUAL_IMAGE}")

    if expected.shape != actual.shape:
        raise Exception(
            f"Image size mismatch.\n"
            f"Expected : {expected.shape}\n"
            f"Actual   : {actual.shape}"
        )

    gray_expected = cv2.cvtColor(expected, cv2.COLOR_BGR2GRAY)
    gray_actual = cv2.cvtColor(actual, cv2.COLOR_BGR2GRAY)

    score, diff = ssim(gray_expected, gray_actual, full=True)

    diff = (diff * 255).astype("uint8")

    _, thresh = cv2.threshold(
        diff,
        0,
        255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    highlighted = actual.copy()

    changed_regions = []

    for i, contour in enumerate(contours):

        if cv2.contourArea(contour) < 30:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        changed_regions.append({
            "id": i + 1,
            "x": x,
            "y": y,
            "width": w,
            "height": h
        })

        cv2.rectangle(
            highlighted,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            2
        )

    cv2.imwrite(str(DIFFERENCE_IMAGE), diff)
    cv2.imwrite(str(HIGHLIGHTED_IMAGE), highlighted)
    cv2.imwrite(str(MASK_IMAGE), thresh)

    return score, changed_regions