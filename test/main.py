from screenshot_capture import capture_screenshot
from compare import compare_images
from component_capture import capture_components
from visual_compare import run_visual_compare

def main():

    print("========== Phase 2 ==========")
    capture_screenshot()

    print("\n========== Phase 3 ==========")
    compare_images()

    print("\n========== Phase 4 ==========")
    capture_components()
    run_visual_compare()


if __name__ == "__main__":
    main()