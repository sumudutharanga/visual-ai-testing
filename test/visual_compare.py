import json
from pathlib import Path

from utils.image_compare import compare_images
from utils.component_mapper import map_components


PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPORT = PROJECT_ROOT / "reports" / "visual_report.json"


def run_visual_compare():

    print("\n========== Phase 6 ==========")

    score, regions = compare_images()
    components = map_components(regions)

    result = {

        "summary": {

            "similarity": round(score * 100, 2),

            "changed_regions": len(regions),

            "changed_components": len(components)

        },

        "components": components

    }

    with open(REPORT, "w") as file:
        json.dump(result, file, indent=4)

    print(f"Similarity : {result['summary']['similarity']}%")
    print(f"Changed Regions : {result['summary']['changed_regions']}")
    print(f"Changed Components : {result['summary']['changed_components']}")
    print("Visual report saved.")