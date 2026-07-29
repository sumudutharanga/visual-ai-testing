import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

LAYOUT_FOLDER = PROJECT_ROOT / "reports" / "layout"


def calculate_iou(region, component):

    rx1 = region["x"]
    ry1 = region["y"]
    rx2 = rx1 + region["width"]
    ry2 = ry1 + region["height"]

    cx1 = component["x"]
    cy1 = component["y"]
    cx2 = cx1 + component["width"]
    cy2 = cy1 + component["height"]

    inter_x1 = max(rx1, cx1)
    inter_y1 = max(ry1, cy1)
    inter_x2 = min(rx2, cx2)
    inter_y2 = min(ry2, cy2)

    if inter_x2 <= inter_x1 or inter_y2 <= inter_y1:
        return 0.0

    intersection = (inter_x2 - inter_x1) * (inter_y2 - inter_y1)

    region_area = region["width"] * region["height"]
    component_area = component["width"] * component["height"]

    union = region_area + component_area - intersection

    return intersection / union


def map_components(regions):

    changed_components = []

    for region in regions:

        matched = False

        for file in LAYOUT_FOLDER.glob("*.json"):

            with open(file) as f:
                component = json.load(f)

            iou = calculate_iou(region, component)

            if iou >= 0.30:
                changed_components.append({

                    "component": file.stem,

                    "iou": round(iou, 3),

                    "region": region

                })

                matched = True

        if not matched:

            changed_components.append({
                "component": "Unknown",
                "region": region
            })

    return changed_components