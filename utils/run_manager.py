from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPORTS = PROJECT_ROOT / "reports"


def get_current_run():

    REPORTS.mkdir(exist_ok=True)

    latest = REPORTS / "latest"

    if latest.exists():

        run_folder = latest.read_text().strip()

        return REPORTS / run_folder

    timestamp = datetime.now().strftime("run_%Y%m%d_%H%M%S")

    run = REPORTS / timestamp

    run.mkdir(parents=True)

    latest.write_text(timestamp)

    return run


def create_run():

    REPORTS.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("run_%Y%m%d_%H%M%S")

    run = REPORTS / timestamp

    run.mkdir(parents=True)

    latest = REPORTS / "latest"

    latest.write_text(timestamp)

    return run