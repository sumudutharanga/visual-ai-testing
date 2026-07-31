import json

from pathlib import Path
import webbrowser

from jinja2 import Environment, FileSystemLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FINAL_REPORT = PROJECT_ROOT / "reports" / "final" / "final_report.json"

OUTPUT = PROJECT_ROOT / "reports" / "final" / "report.html"

TEMPLATE_FOLDER = PROJECT_ROOT / "templates"

env = Environment(

    loader=FileSystemLoader(TEMPLATE_FOLDER)

)

template = env.get_template("report.html")


def generate_html():

    with open(FINAL_REPORT) as f:

        report = json.load(f)

    html = template.render(

        summary=report["summary"],

        components=report["components"]

    )

    with open(OUTPUT, "w", encoding="utf-8") as f:

        f.write(html)

    print("HTML Report Saved :", OUTPUT)
    #print("HTML Report Saved :", OUTPUT)

    # Automatically open the report
    webbrowser.open(OUTPUT.resolve().as_uri())