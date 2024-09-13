from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import argparse
import math


def screenshot(file: str, output_dir: str, browser, max_height) -> None:
    if browser == "chrome":
        # Set up Chrome in headless mode
        op = webdriver.ChromeOptions()
        op.add_argument("headless")
        driver = webdriver.Chrome(options=op)
        source = ""
    else:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        source = "view-source:"

    # Read the file, get line count and find the longest line
    with open(file, "r") as f:
        lines = f.readlines()
        line_count = len(lines)
        longest_line = max(lines, key=len)  # Find the longest line

    # Dynamic height based on line count
    line_height = 20  # Assume each line requires about 20px of height
    min_height = 600  # Minimum window height to avoid too small windows
    calculated_height = max(min_height, line_count * line_height)

    # Dynamic width based on the longest line
    char_width = (
        6  # Approximate pixel width per character (depends on font size and type)
    )
    min_width = 800  # Minimum window width
    calculated_width = max(min_width, len(longest_line) * char_width)

    # Set window width and initial height (cap it to max_height)
    driver.set_window_size(calculated_width, min(max_height, calculated_height))

    # Load the file as source in browser
    url = f"{source}file://{file}"
    driver.get(url)

    # Adjust zoom level if necessary
    driver.execute_script("document.body.style.zoom='125%'")

    if "/" in file:
        file = file.split("/")[-1]

    save_location = output_dir + file

    # Calculate the number of height sections if the content exceeds max_height
    if calculated_height > max_height:
        height_sections = math.ceil(calculated_height / max_height)

        # Loop through each section and take a screenshot
        for section in range(height_sections):
            # Scroll to the appropriate section of the page
            driver.execute_script(f"window.scrollTo(0, {section * max_height})")

            # Save screenshot for the current section
            screenshot_filename = f"{save_location}_part{section + 1}.png"
            driver.save_screenshot(screenshot_filename)
            print(f"Saved {screenshot_filename}")
    else:
        # If the calculated height is within the max height, take one screenshot
        driver.save_screenshot(f"{save_location}.png")
        print(f"Saved {save_location}.png")

    # Quit the driver after taking screenshots
    driver.quit()


def main():
    # Argument parser for file input
    parser = argparse.ArgumentParser("""python3 file-screenshot.py myfile""")
    parser.add_argument("file", action="store", help="myfile")
    parser.add_argument(
        "-O",
        "--output-folder",
        action="store",
        help="Output folder",
        default="./screenshots/",
        required=False,
    )
    parser.add_argument(
        "-B",
        "--browser",
        action="store",
        help="Browser you want to use",
        default="firefox",
        choices=["firefox", "chrome"],
        required=False,
    )
    parser.add_argument(
        "-M",
        "--max-height",
        action="store",
        help="The max height of your screenshot(s)",
        default=1080,
        required=False,
    )
    args = parser.parse_args()

    # Get absolute file path
    user_file = os.path.abspath(args.file)

    output_dir = args.output_folder
    if output_dir[-1] != "/":
        output_dir = output_dir + "/"

    screenshot(user_file, output_dir, args.browser, args.max_height)


if __name__ == "__main__":
    main()
