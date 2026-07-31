from screenshot_capture import capture_screenshot
from compare import compare_images
from component_capture import capture_components
from visual_compare import run_visual_compare
from utils.run_manager import create_run
from component_analyzer_runner import run_component_analysis
from validator_runner import run_validation
from ai_runner import run_ai_analysis
from final_report_runner import run_final_report
from html_report_runner import run_html_report
from figma_parser_runner import run_figma_parser


def main():
    capture_screenshot()
    compare_images()
    capture_components()
    run_visual_compare()
    run_component_analysis()

    # Generate expected values from Figma JSON
    run_figma_parser()

    run_validation()
    run_ai_analysis()
    run_final_report()
    run_html_report()


if __name__ == "__main__":
    main()