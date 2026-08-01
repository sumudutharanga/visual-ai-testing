from utils.run_cleanup import clean_previous_run

from screenshot_capture import capture_screenshot
from compare import compare_images
from component_capture import capture_components
from visual_compare import run_visual_compare
from component_analyzer_runner import run_component_analysis
from figma_parser_runner import run_figma_parser
from validator_runner import run_validation
from ai_runner import run_ai_analysis
from final_report_runner import run_final_report
from html_report_runner import run_html_report
from jira_runner import run_jira_integration


def main():
    clean_previous_run()

    capture_screenshot()
    compare_images()
    capture_components()
    run_visual_compare()
    run_component_analysis()
    run_figma_parser()
    run_validation()
    run_ai_analysis()

    # Creates final_report.json
    run_final_report()

    # Reads final_report.json and creates Jira tickets
    run_jira_integration()

    # Generates and opens HTML
    run_html_report()


if __name__ == "__main__":
    main()