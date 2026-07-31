import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_FILE = PROJECT_ROOT / "expected" / "upload_modal.json"
COMPONENT_FOLDER = PROJECT_ROOT / "reports" / "components"
VALIDATION_FOLDER = PROJECT_ROOT / "reports" / "validation"

VALIDATION_FOLDER.mkdir(parents=True, exist_ok=True)


DOM_PROPERTIES = {
    "text",
    "visible",
    "enabled",
    "tag",
    "placeholder",
    "value"
}

LAYOUT_PROPERTIES = {
    "x",
    "y",
    "width",
    "height"
}


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()

    return value


def find_actual_value(component: dict, property_name: str) -> Any:
    if property_name in DOM_PROPERTIES:
        return (component.get("dom") or {}).get(property_name)

    if property_name in LAYOUT_PROPERTIES:
        return (component.get("layout") or {}).get(property_name)

    return (component.get("css") or {}).get(property_name)


def compare_values(property_name: str, expected: Any, actual: Any) -> bool:
    if property_name in LAYOUT_PROPERTIES:
        try:
            return abs(float(expected) - float(actual)) <= 1
        except (TypeError, ValueError):
            return False

    return normalize(expected) == normalize(actual)


def validate():
    expected_rules = load_json(EXPECTED_FILE)

    if expected_rules is None:
        raise FileNotFoundError(f"Expected file not found: {EXPECTED_FILE}")

    actual_components = {
        file.stem: load_json(file)
        for file in COMPONENT_FOLDER.glob("*.json")
    }

    all_component_names = sorted(
        set(actual_components.keys()) | set(expected_rules.keys())
    )

    for name in all_component_names:
        actual_component = actual_components.get(name)
        rules = expected_rules.get(name)

        result = {
            "component": name,
            "status": "PASS",
            "checks": {}
        }

        if rules is None:
            result["status"] = "NOT_CONFIGURED"
            result["checks"]["configuration"] = {
                "status": "NOT_CONFIGURED",
                "expected": "Component should have Figma rules",
                "actual": "No Figma mapping found"
            }

        elif actual_component is None:
            result["status"] = "FAIL"
            result["checks"]["component"] = {
                "status": "FAIL",
                "expected": "Component exists",
                "actual": "Component report missing"
            }

        else:
            for property_name, expected_value in rules.items():
                actual_value = find_actual_value(
                    actual_component,
                    property_name
                )

                passed = compare_values(
                    property_name,
                    expected_value,
                    actual_value
                )

                check_status = "PASS" if passed else "FAIL"

                result["checks"][property_name] = {
                    "status": check_status,
                    "expected": expected_value,
                    "actual": actual_value
                }

                if not passed:
                    result["status"] = "FAIL"

        output = VALIDATION_FOLDER / f"{name}.json"

        with output.open("w", encoding="utf-8") as file:
            json.dump(result, file, indent=4)

        print(f"Validation saved: {output.name}")