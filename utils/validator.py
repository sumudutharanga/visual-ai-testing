import json
from pathlib import Path
from typing import Any

from config.settings import PIXEL_TOLERANCE


PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_FILE = PROJECT_ROOT / "expected" / "upload_modal.json"
COMPONENT_FOLDER = PROJECT_ROOT / "reports" / "components"
VALIDATION_FOLDER = PROJECT_ROOT / "reports" / "validation"


DOM_PROPERTIES = {
    "text",
    "visible",
    "enabled",
    "tag",
    "placeholder",
    "value",
}

LAYOUT_PROPERTIES = {
    "x",
    "y",
    "width",
    "height",
}

PIXEL_PROPERTIES = {
    "x",
    "y",
    "width",
    "height",
    "lineHeight",
    "paddingTop",
    "paddingRight",
    "paddingBottom",
    "paddingLeft",
    "marginTop",
    "marginRight",
    "marginBottom",
    "marginLeft",
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

def normalize_font_family(value: Any) -> list[str]:
    if not isinstance(value, str):
        return []

    families = []

    for item in value.split(","):
        cleaned = item.strip().strip('"').strip("'").lower()

        if cleaned:
            families.append(cleaned)

    return families


def parse_pixel_value(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        cleaned = value.strip().lower()

        if cleaned.endswith("px"):
            cleaned = cleaned[:-2].strip()

        try:
            return float(cleaned)
        except ValueError:
            return None

    return None


def find_actual_value(
    component: dict,
    property_name: str,
) -> Any:
    if property_name in DOM_PROPERTIES:
        return (component.get("dom") or {}).get(property_name)

    if property_name in LAYOUT_PROPERTIES:
        return (component.get("layout") or {}).get(property_name)

    return (component.get("css") or {}).get(property_name)


def compare_values(
    property_name: str,
    expected: Any,
    actual: Any,
) -> tuple[bool, float | None]:
    if property_name == "fontFamily":
        expected_fonts = normalize_font_family(expected)
        actual_fonts = normalize_font_family(actual)

        if not expected_fonts or not actual_fonts:
            return False, None

        expected_primary = expected_fonts[0]

        return expected_primary in actual_fonts, None

    if property_name in PIXEL_PROPERTIES:
        expected_number = parse_pixel_value(expected)
        actual_number = parse_pixel_value(actual)

        if expected_number is None or actual_number is None:
            return False, None

        difference = abs(expected_number - actual_number)

        return difference <= PIXEL_TOLERANCE, difference

    return normalize(expected) == normalize(actual), None


def validate() -> None:
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Expected file: {EXPECTED_FILE}")
    print(f"Components folder: {COMPONENT_FOLDER}")
    print(f"Validation output: {VALIDATION_FOLDER}")

    VALIDATION_FOLDER.mkdir(parents=True, exist_ok=True)

    expected_rules = load_json(EXPECTED_FILE)

    if expected_rules is None:
        raise FileNotFoundError(
            f"Expected rules file not found: {EXPECTED_FILE}"
        )

    if not isinstance(expected_rules, dict):
        raise TypeError(
            "Expected rules must be a JSON object containing "
            "component names."
        )

    component_files = sorted(
        COMPONENT_FOLDER.glob("*.json")
    )

    if not component_files:
        raise RuntimeError(
            f"No component reports found in: {COMPONENT_FOLDER}"
        )

    print(
        f"Expected Figma components found: "
        f"{len(expected_rules)}"
    )
    print(
        f"Actual component reports found: "
        f"{len(component_files)}"
    )

    actual_components = {}

    for component_file in component_files:
        component_data = load_json(component_file)

        if component_data is None:
            print(
                f"Skipping unreadable component file: "
                f"{component_file}"
            )
            continue

        actual_components[component_file.stem] = component_data

    all_component_names = sorted(
        set(actual_components.keys())
        | set(expected_rules.keys())
    )

    if not all_component_names:
        raise RuntimeError(
            "No expected or actual components were found."
        )

    generated_count = 0

    for name in all_component_names:
        print(f"Validating component: {name}")

        actual_component = actual_components.get(name)
        rules = expected_rules.get(name)

        result = {
            "component": name,
            "status": "PASS",
            "checks": {},
        }

        if rules is None:
            result["status"] = "NOT_CONFIGURED"

            result["checks"]["configuration"] = {
                "status": "NOT_CONFIGURED",
                "expected": "Figma rules configured",
                "actual": "No matching Figma mapping",
            }

        elif actual_component is None:
            result["status"] = "FAIL"

            result["checks"]["component"] = {
                "status": "FAIL",
                "expected": "Component report exists",
                "actual": "Component report missing",
            }

        elif not isinstance(rules, dict):
            result["status"] = "FAIL"

            result["checks"]["configuration"] = {
                "status": "FAIL",
                "expected": "Rules must be a JSON object",
                "actual": type(rules).__name__,
            }

        else:
            for property_name, expected_value in rules.items():
                actual_value = find_actual_value(
                    actual_component,
                    property_name,
                )

                passed, difference = compare_values(
                    property_name,
                    expected_value,
                    actual_value,
                )

                check_result = {
                    "status": "PASS" if passed else "FAIL",
                    "expected": expected_value,
                    "actual": actual_value,
                }

                if difference is not None:
                    check_result["difference_px"] = round(
                        difference,
                        3,
                    )
                    check_result["tolerance_px"] = (
                        PIXEL_TOLERANCE
                    )

                result["checks"][property_name] = check_result

                if not passed:
                    result["status"] = "FAIL"

        output_file = VALIDATION_FOLDER / f"{name}.json"

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(result, file, indent=4)

        generated_count += 1
        print(f"Validation saved: {output_file.name}")

    if generated_count == 0:
        raise RuntimeError(
            "Validator completed without generating reports."
        )

    print(
        f"Generated {generated_count} validation reports."
    )