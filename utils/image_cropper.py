from pathlib import Path
import cv2

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_IMAGE = PROJECT_ROOT / "figma" / "expected" / "upload_modal.png"
ACTUAL_IMAGE = PROJECT_ROOT / "screenshots" / "actual.png"

EXPECTED_OUTPUT = PROJECT_ROOT / "reports" / "cropped" / "expected"
ACTUAL_OUTPUT = PROJECT_ROOT / "reports" / "cropped" / "actual"

EXPECTED_OUTPUT.mkdir(parents=True, exist_ok=True)
ACTUAL_OUTPUT.mkdir(parents=True, exist_ok=True)
EXPECTED_OUTPUT.mkdir(parents=True, exist_ok=True)
ACTUAL_OUTPUT.mkdir(parents=True, exist_ok=True)


def crop_component(component_name, box):
    expected = cv2.imread(str(EXPECTED_IMAGE))
    actual = cv2.imread(str(ACTUAL_IMAGE))
    if expected is None:
        print("Expected image not found.")
        return

    if actual is None:
        print("Actual image not found.")
        return

    x = int(box["x"])
    y = int(box["y"])
    w = int(box["width"])
    h = int(box["height"])

    expected_crop = expected[y:y+h, x:x+w]
    actual_crop = actual[y:y+h, x:x+w]

    cv2.imwrite(
        str(EXPECTED_OUTPUT / f"{component_name}.png"),
        expected_crop
    )

    cv2.imwrite(
        str(ACTUAL_OUTPUT / f"{component_name}.png"),
        actual_crop
    )

    print(f"✓ Cropped {component_name}")