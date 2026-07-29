from pathlib import Path
import json

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# reports/layout
OUTPUT_FOLDER = PROJECT_ROOT / "reports" / "layout"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


def save_layout(name, box):
    file = OUTPUT_FOLDER / f"{name}.json"

    with open(file, "w") as f:
        json.dump(box, f, indent=4)

    print(f"Layout saved : {file}")