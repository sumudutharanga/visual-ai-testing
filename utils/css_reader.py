import json
from pathlib import Path

from config.settings import (
    VIEWPORT_WIDTH,
    VIEWPORT_HEIGHT,
    SCREENSHOT_FOLDER,
    REPORT_FOLDER
)


CSS_REPORT_FOLDER = REPORT_FOLDER/"css"
CSS_REPORT_FOLDER.mkdir(parents=True, exist_ok=True)


def get_css_properties(page, test_id):

    element = page.get_by_test_id(test_id)

    css = element.evaluate("""
    (el) => {

        const style = window.getComputedStyle(el);
        const rect = el.getBoundingClientRect();

        return {

            width: rect.width,
            height: rect.height,

            x: rect.x,
            y: rect.y,

            fontFamily: style.fontFamily,
            fontSize: style.fontSize,
            fontWeight: style.fontWeight,
            lineHeight: style.lineHeight,

            color: style.color,
            backgroundColor: style.backgroundColor,

            borderRadius: style.borderRadius,

            paddingTop: style.paddingTop,
            paddingRight: style.paddingRight,
            paddingBottom: style.paddingBottom,
            paddingLeft: style.paddingLeft,

            marginTop: style.marginTop,
            marginRight: style.marginRight,
            marginBottom: style.marginBottom,
            marginLeft: style.marginLeft
        };

    }
    """)

    return css


def save_css_report(component_name, css_data):

    report_file = CSS_REPORT_FOLDER / f"{component_name}.json"

    with open(report_file, "w") as file:
        json.dump(css_data, file, indent=4)

    print(f"CSS Report Saved : {report_file}")