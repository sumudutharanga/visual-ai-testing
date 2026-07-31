import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSS_FOLDER = PROJECT_ROOT / "reports" / "css"
DOM_FOLDER = PROJECT_ROOT / "reports" / "dom"
LAYOUT_FOLDER = PROJECT_ROOT / "reports" / "layout"
COMPONENT_FOLDER = PROJECT_ROOT / "reports" / "components"
VISUAL_REPORT = PROJECT_ROOT / "reports" / "visual_report.json"

COMPONENT_FOLDER.mkdir(parents=True, exist_ok=True)


def load_json(path):
    if not path.exists():
        return None

    with open(path, "r") as f:
        return json.load(f)


def analyze_components():

    visual = load_json(VISUAL_REPORT)

    if visual is None:
        print("visual_report.json not found.")
        return

    changed = {}

    for item in visual["components"]:
        changed[item["component"]] = item

    for css_file in CSS_FOLDER.glob("*.json"):

        name = css_file.stem

        component = {

            "component": name,

            "layout": load_json(LAYOUT_FOLDER / f"{name}.json"),

            "css": load_json(CSS_FOLDER / f"{name}.json"),

            "dom": load_json(DOM_FOLDER / f"{name}.json"),

            "visual": changed.get(
                name,
                {
                    "changed": False
                }
            )

        }

        output = COMPONENT_FOLDER / f"{name}.json"

        with open(output, "w") as f:
            json.dump(component, f, indent=4)

        print(f"✓ Component Report Saved : {output.name}")