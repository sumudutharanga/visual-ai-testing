from utils.jira_payload_builder import (
    build_jira_payload,
)
from utils.n8n_client import send_tickets_to_n8n


def run_jira_integration() -> None:
    print("\n========== PHASE 11: JIRA ==========")

    payload = build_jira_payload()

    results = send_tickets_to_n8n(payload)

    print(
        f"Jira issues created: "
        f"{len(results.get('created', []))}"
    )

    print(
        f"Jira issues failed: "
        f"{len(results.get('failed', []))}"
    )

    print("Jira integration completed.")

    if __name__ == "__main__":
        run_jira_integration()