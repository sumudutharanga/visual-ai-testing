import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent

FINAL_REPORT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "final"
    / "final_report.json"
)

JIRA_REPORT_FOLDER = PROJECT_ROOT / "reports" / "jira"
JIRA_PAYLOAD_FILE = JIRA_REPORT_FOLDER / "jira_payload.json"

JIRA_REPORT_FOLDER.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Required report not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def readable_component_name(component_name: str) -> str:
    return component_name.replace("_", " ").title()


def highest_severity(issues: list[dict[str, Any]]) -> str:
    severity_rank = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4,
    }

    highest = "Medium"

    for issue in issues:
        severity = issue.get("severity", "Medium")

        if severity_rank.get(severity, 2) > severity_rank.get(highest, 2):
            highest = severity

    return highest


def build_issue_description(
    component_name: str,
    issues: list[dict[str, Any]],
    similarity: float | int | None,
) -> str:
    lines = [
        "Visual AI automated UI validation failure",
        "",
        f"Component: {component_name}",
        f"Overall visual similarity: {similarity}%",
        "",
        "Failed checks:",
    ]

    if not issues:
        lines.extend(
            [
                "",
                "No detailed AI issue report was available.",
                "Review the validation and visual reports.",
            ]
        )

        return "\n".join(lines)

    for index, issue in enumerate(issues, start=1):
        lines.extend(
            [
                "",
                f"{index}. Property: {issue.get('property', 'Unknown')}",
                f"   Expected: {issue.get('expected')}",
                f"   Actual: {issue.get('actual')}",
                f"   Reason: {issue.get('reason', 'Value mismatch')}",
                f"   Suggestion: {issue.get('suggestion', 'Review the component')}",
                f"   Severity: {issue.get('severity', 'Medium')}",
            ]
        )

    return "\n".join(lines)


def build_jira_payload() -> dict[str, Any]:
    report = load_json(FINAL_REPORT_FILE)

    summary = report.get("summary", {})
    similarity = summary.get("similarity", 0)

    tickets: list[dict[str, Any]] = []

    for component in report.get("components", []):
        validation = component.get("validation") or {}
        ai_report = component.get("ai") or {}

        if validation.get("status") != "FAIL":
            continue

        component_name = component.get("component", "unknown_component")
        readable_name = readable_component_name(component_name)

        issues = ai_report.get("issues") or []
        severity = highest_severity(issues)

        ticket = {
            "summary": (
                f"[Visual AI] {readable_name} does not match "
                f"the Figma design"
            ),
            "description": build_issue_description(
                component_name=component_name,
                issues=issues,
                similarity=similarity,
            ),
            "component": component_name,
            "severity": severity,
        }

        tickets.append(ticket)

    payload = {
        "total_failed_components": len(tickets),
        "tickets": tickets,
    }

    with JIRA_PAYLOAD_FILE.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=4)

    print(f"Jira payload saved: {JIRA_PAYLOAD_FILE}")
    print(f"Jira tickets prepared: {len(tickets)}")

    return payload