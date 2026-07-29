import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT = PROJECT_ROOT / "reports" / "dom"
OUTPUT.mkdir(parents=True, exist_ok=True)


def save_dom_info(name, info):
    file = OUTPUT / f"{name}.json"

    with open(file, "w") as f:
        json.dump(info, f, indent=4)

    print(f"DOM Report Saved : {file}")