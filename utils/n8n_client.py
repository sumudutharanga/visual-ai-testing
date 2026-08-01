import json
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

JIRA_REPORT_FOLDER = PROJECT_ROOT / "reports" / "jira"
JIRA_RESULTS_FILE = JIRA_REPORT_FOLDER / "jira_results.json"

JIRA_REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

load_dotenv(PROJECT_ROOT / ".env")


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def send_tickets_to_n8n(
    payload: dict[str, Any],
) -> dict[str, Any]:

    create_tickets = env_flag(
        "CREATE_JIRA_TICKETS",
        default=False,
    )

    if not create_tickets:
        result = {
            "status": "SKIPPED",
            "message": (
                "Jira ticket creation is disabled in .env."
            ),
            "created": [],
            "failed": [],
        }

        save_results(result)
        print(result["message"])

        return result

    webhook_url = os.getenv("N8N_JIRA_WEBHOOK_URL")

    if not webhook_url:
        raise RuntimeError(
            "N8N_JIRA_WEBHOOK_URL is missing from .env"
        )

    tickets = payload.get("tickets", [])

    result: dict[str, Any] = {
        "status": "COMPLETED",
        "requested": len(tickets),
        "created": [],
        "failed": [],
    }

    if not tickets:
        result["message"] = (
            "No failed components were found. "
            "No Jira tickets were created."
        )

        save_results(result)
        print(result["message"])

        return result

    for ticket in tickets:
        component = ticket.get(
            "component",
            "unknown_component",
        )

        print(f"Sending Jira request: {component}")

        try:
            response = requests.post(
                webhook_url,
                json=ticket,
                timeout=30,
            )

            response.raise_for_status()

            try:
                response_data = response.json()
            except ValueError:
                response_data = {
                    "raw_response": response.text
                }

            if response_data.get("success") is True:
                result["created"].append(
                    {
                        "component": component,
                        "jira_key": response_data.get(
                            "jira_key"
                        ),
                        "jira_id": response_data.get(
                            "jira_id"
                        ),
                        "summary": ticket.get("summary"),
                    }
                )

                print(
                    f"Jira issue created: "
                    f"{response_data.get('jira_key')}"
                )

            else:
                result["failed"].append(
                    {
                        "component": component,
                        "error": (
                            "n8n did not return success=true"
                        ),
                        "response": response_data,
                    }
                )

                print(
                    f"Jira creation failed for: "
                    f"{component}"
                )

        except requests.RequestException as error:
            result["failed"].append(
                {
                    "component": component,
                    "error": str(error),
                }
            )

            print(
                f"n8n request failed for "
                f"{component}: {error}"
            )

    if result["failed"]:
        result["status"] = "PARTIAL_FAILURE"

    save_results(result)

    return result


def save_results(result: dict[str, Any]) -> None:
    with JIRA_RESULTS_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(result, file, indent=4)

    print(f"Jira results saved: {JIRA_RESULTS_FILE}")