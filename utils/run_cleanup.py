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
    PROJECT_ROOT / "reports" / "jira",
    PROJECT_ROOT / "screenshots" / "components",
]


GENERATED_FILES = [
    PROJECT_ROOT / "screenshots" / "actual.png",
    PROJECT_ROOT / "reports" / "difference.png",
    PROJECT_ROOT / "reports" / "highlighted.png",
    PROJECT_ROOT / "reports" / "mask.png",
    PROJECT_ROOT / "reports" / "visual_report.json",
]


def clean_previous_run() -> None:
    print("Cleaning previous generated results...")

    # Delete and recreate generated folders
    for folder in GENERATED_FOLDERS:
        if folder.exists():
            shutil.rmtree(folder)

        folder.mkdir(parents=True, exist_ok=True)

    # Delete generated files
    for file_path in GENERATED_FILES:
        if file_path.exists():
            if file_path.is_file():
                file_path.unlink()
            elif file_path.is_dir():
                shutil.rmtree(file_path)

    print("Previous generated results removed.")