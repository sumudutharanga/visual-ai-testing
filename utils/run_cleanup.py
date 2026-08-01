import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

GENERATED_FOLDERS = [
    PROJECT_ROOT / "reports" / "css",
    PROJECT_ROOT / "reports" / "dom",
    PROJECT_ROOT / "reports" / "layout",
    PROJECT_ROOT / "reports" / "components",
    PROJECT_ROOT / "reports" / "validation",
    PROJECT_ROOT / "reports" / "ai",
    PROJECT_ROOT / "reports" / "final",
    PROJECT_ROOT / "screenshots" / "components",
]

GENERATED_FILES = [
    PROJECT_ROOT / "screenshots" / "actual.png",
    PROJECT_ROOT / "reports" / "difference.png",
    PROJECT_ROOT / "reports" / "highlighted.png",
    PROJECT_ROOT / "reports" / "mask.png",
    PROJECT_ROOT / "reports" / "visual_report.json",
    PROJECT_ROOT / "reports" / "jira",
]


def clean_previous_run() -> None:
    print("\nCleaning previous generated results...")

    for folder in GENERATED_FOLDERS:
        if folder.exists():
            shutil.rmtree(folder)

        folder.mkdir(parents=True, exist_ok=True)

    for file_path in GENERATED_FILES:
        if file_path.exists():
            file_path.unlink()

    print("Previous generated results removed.")