import cv2
import os

from skimage.metrics import structural_similarity as ssim

from config.settings import (
    EXPECTED_IMAGE,
    SCREENSHOT_FOLDER,
    SCREENSHOT_NAME,
    REPORT_FOLDER
)


def compare_images():

    print("\nStarting image comparison...")

    expected_path = EXPECTED_IMAGE
    actual_path = SCREENSHOT_FOLDER / SCREENSHOT_NAME

    # Check if files exist
    if not expected_path.exists():
        print(f"Expected image not found:\n{expected_path}")
        return

    if not actual_path.exists():
        print(f"Actual screenshot not found:\n{actual_path}")
        return

    # Read images
    expected = cv2.imread(str(expected_path))
    actual = cv2.imread(str(actual_path))

    if expected is None or actual is None:
        print("Failed to load one or both images.")
        return

    # Check image size
    if expected.shape != actual.shape:
        print("Image sizes are different.")
        print(f"Expected : {expected.shape}")
        print(f"Actual   : {actual.shape}")
        return

    # Convert to grayscale
    gray_expected = cv2.cvtColor(expected, cv2.COLOR_BGR2GRAY)
    gray_actual = cv2.cvtColor(actual, cv2.COLOR_BGR2GRAY)

    # SSIM Comparison
    score, diff = ssim(
        gray_expected,
        gray_actual,
        full=True
    )

    print(f"\nSimilarity Score : {score * 100:.2f}%")

    # Convert difference image
    diff = (diff * 255).astype("uint8")

    # Threshold
    thresh = cv2.threshold(
        diff,
        0,
        255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    )[1]

    # Find contours
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    total_changes = 0

    for contour in contours:

        # Ignore tiny noise
        if cv2.contourArea(contour) < 40:
            continue

        total_changes += 1

        x, y, w, h = cv2.boundingRect(contour)

        cv2.rectangle(
            actual,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            2
        )

    # Create report folder
    os.makedirs(REPORT_FOLDER, exist_ok=True)

    report_path = REPORT_FOLDER / "difference.png"

    cv2.imwrite(str(report_path), actual)

    print(f"Detected Regions : {total_changes}")
    print(f"Report Saved     : {report_path}")

    if score > 0.99:
        print("\nPASS - Images are almost identical.")
    else:
        print("\nFAIL - Differences detected.")