import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

VALIDATION_FOLDER = PROJECT_ROOT / "reports" / "validation"
AI_FOLDER = PROJECT_ROOT / "reports" / "ai"

AI_FOLDER.mkdir(parents=True, exist_ok=True)


ISSUE_RULES = {
    "text": (
        "The displayed text differs from the Figma design.",
        "Update the displayed text to exactly match the expected text.",
        "High"
    ),
    "visible": (
        "The component visibility differs from the expected state.",
        "Review rendering conditions and CSS visibility.",
        "High"
    ),
    "enabled": (
        "The component enabled state differs from the expected state.",
        "Review the business logic controlling the component state.",
        "High"
    ),
    "fontSize": (
        "The font size differs from the Figma typography specification.",
        "Update the CSS font-size to the expected value.",
        "Medium"
    ),
    "fontWeight": (
        "The font weight differs from the Figma typography specification.",
        "Update the CSS font-weight to the expected value.",
        "Medium"
    ),
    "fontFamily": (
        "The font family differs from the Figma design.",
        "Apply the expected font family or design-system typography token.",
        "Medium"
    ),
    "color": (
        "The text color differs from the Figma design.",
        "Update the CSS color to the expected value.",
        "Medium"
    ),
    "backgroundColor": (
        "The background color differs from the Figma design.",
        "Update the background color to the expected value.",
        "Medium"
    ),
    "borderRadius": (
        "The corner radius differs from the Figma design.",
        "Update border-radius to the expected value.",
        "Low"
    ),
    "width": (
        "The component width differs from the Figma design.",
        "Review width, padding, and box-sizing.",
        "Medium"
    ),
    "height": (
        "The component height differs from the Figma design.",
        "Review height, padding, line-height, and box-sizing.",
        "Medium"
    )
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def analyze():
    validation_files = sorted(VALIDATION_FOLDER.glob("*.json"))

    for file in validation_files:
        validation = load_json(file)

        report = {
            "component": validation["component"],
            "status": validation["status"],
            "issues": []
        }

        for property_name, check in validation.get("checks", {}).items():
            if check.get("status") not in {"FAIL", "NOT_CONFIGURED"}:
                continue

            reason, suggestion, severity = ISSUE_RULES.get(
                property_name,
                (
                    "The actual value differs from the expected value.",
                    "Review this property and update it to match the design.",
                    "Medium"
                )
            )

            expected = check.get("expected")
            actual = check.get("actual")

            report["issues"].append({
                "property": property_name,
                "expected": expected,
                "actual": actual,
                "reason": reason,
                "suggestion": suggestion,
                "severity": severity
            })

        if report["status"] == "FAIL" and not report["issues"]:
            report["issues"].append({
                "property": "internal_report",
                "expected": "At least one failed validation check",
                "actual": "No failed check details found",
                "reason": "The validation report is incomplete.",
                "suggestion": "Review the generated validation JSON.",
                "severity": "High"
            })

        output = AI_FOLDER / file.name

        with output.open("w", encoding="utf-8") as file_handle:
            json.dump(report, file_handle, indent=4)

        print(f"AI report saved: {output.name}")