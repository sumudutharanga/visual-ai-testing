import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPORTS = PROJECT_ROOT / "reports"

COMPONENT_FOLDER = REPORTS / "components"
VALIDATION_FOLDER = REPORTS / "validation"
AI_FOLDER = REPORTS / "ai"

VISUAL_REPORT = REPORTS / "visual_report.json"

FINAL_FOLDER = REPORTS / "final"
FINAL_FOLDER.mkdir(parents=True, exist_ok=True)

FINAL_REPORT = FINAL_FOLDER / "final_report.json"


def load_json(path: Path) -> dict[str, Any] | None:
    """
    Load a JSON file.

    Returns None when the file does not exist.
    """

    if not path.exists():
        return None

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        print(f"Invalid JSON file: {path}")
        print(error)
        return None


def get_similarity() -> float:
    """
    Read the overall visual similarity from visual_report.json.
    """

    visual_report = load_json(VISUAL_REPORT)

    if not visual_report:
        return 0.0

    summary = visual_report.get("summary", {})

    return summary.get(
        "similarity",
        visual_report.get("similarity", 0.0)
    )


def get_all_component_names() -> list[str]:
    """
    Collect component names from component, validation, and AI reports.

    This prevents a component from disappearing when one report file
    is missing from another folder.
    """

    component_names: set[str] = set()

    if COMPONENT_FOLDER.exists():
        component_names.update(
            file.stem
            for file in COMPONENT_FOLDER.glob("*.json")
        )

    if VALIDATION_FOLDER.exists():
        component_names.update(
            file.stem
            for file in VALIDATION_FOLDER.glob("*.json")
        )

    if AI_FOLDER.exists():
        component_names.update(
            file.stem
            for file in AI_FOLDER.glob("*.json")
        )

    return sorted(component_names)


def get_component_status(
    validation: dict[str, Any] | None
) -> str:
    """
    Return a safe component status.
    """

    if validation is None:
        return "MISSING"

    return validation.get("status", "MISSING")


def build_final_report() -> Path:
    """
    Merge component, validation, AI, and visual reports into one file.
    """

    components: list[dict[str, Any]] = []

    passed = 0
    failed = 0
    not_configured = 0
    missing = 0

    component_names = get_all_component_names()

    for name in component_names:
        component = (
            load_json(COMPONENT_FOLDER / f"{name}.json")
            or {}
        )

        validation = load_json(
            VALIDATION_FOLDER / f"{name}.json"
        )

        ai = load_json(
            AI_FOLDER / f"{name}.json"
        )

        status = get_component_status(validation)

        if status == "PASS":
            passed += 1

        elif status == "FAIL":
            failed += 1

        elif status == "NOT_CONFIGURED":
            not_configured += 1

        else:
            missing += 1

        components.append(
            {
                "component": name,
                "status": status,

                "layout": component.get("layout"),
                "css": component.get("css"),
                "dom": component.get("dom"),
                "visual": component.get("visual"),

                "validation": validation,
                "ai": ai
            }
        )

    total_components = len(component_names)

    report = {
        "summary": {
            "total_components": total_components,
            "passed": passed,
            "failed": failed,
            "not_configured": not_configured,
            "missing_reports": missing,
            "similarity": get_similarity()
        },

        "components": components
    }

    with FINAL_REPORT.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Final Report Saved : {FINAL_REPORT}")
    print(f"Total Components   : {total_components}")
    print(f"Passed             : {passed}")
    print(f"Failed             : {failed}")
    print(f"Not Configured     : {not_configured}")
    print(f"Missing Reports    : {missing}")

    return FINAL_REPORT