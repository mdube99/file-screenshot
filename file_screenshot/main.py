from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PIL import Image
import os
import argparse
import time

line_height = 20


def split_image_vertically(image_path: str, max_height: int, output_dir: str) -> None:
    # Open the image
    img = Image.open(image_path)

    # # get image name only
    image_path = image_path.split("/")[-1]
    image_path = image_path.split(".")[0]

    # Get image dimensions
    width, height = img.size

    # List to store split images
    split_images = []

    # Initialize the starting point
    upper = 8

    while upper < height:
        # Calculate the lower boundary, ensuring we align it to a full line of text
        lower = upper + max_height

        # If lower goes beyond image height, adjust it to image height
        if lower > height:
            lower = height
        else:
            # Ensure the lower boundary is aligned with the bottom of a line
            remainder = lower % line_height
            if remainder != 0:
                lower -= remainder  # Move lower up to align with a full line

        # Ensure that we are not creating zero-height splits
        if lower <= upper:
            break

        # Define the cropping box (left, upper, right, lower)
        box = (0, upper, width, lower)

        # Crop the image
        split_image = img.crop(box)
        split_images.append(split_image)

        # Move the upper boundary for the next split
        upper = lower

    for idx, split_img in enumerate(split_images):
        split_img.save(f"{output_dir}./{image_path}_split_{idx}.png", "PNG")
    print(f"[+] Split screenshot '{image_path}' into {len(split_images)} parts.")


def screenshot(file: str, output_dir: str, browser: str) -> str:
    # Get absolute file path
    file = os.path.abspath(file)

    if browser == "chrome":
        # Set up Chrome in headless mode
        op = webdriver.ChromeOptions()
        op.add_argument("headless")
        driver = webdriver.Chrome(options=op)

        # `view-source:` in chrome adds a "line wrap" option that shows up in all screenshots.
        # haven't figured out a way around this, so i just don't bother
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
    min_height = 20  # Minimum window height to avoid too small windows
    # calculated_height = max(min_height, line_count * line_height)
    calculated_height = max(min_height, (line_count + 6) * line_height)

    # Dynamic width based on the longest line
    char_width = (
        6  # Approximate pixel width per character (depends on font size and type)
    )
    min_width = 400  # Minimum window width
    calculated_width = max(min_width, len(longest_line) * char_width)

    # Set window width and initial height (cap it to max_height)
    driver.set_window_size(calculated_width, calculated_height)

    # Load the file as source in browser
    url = f"{source}file://{file}"
    driver.get(url)

    # Adjust zoom level if necessary
    driver.execute_script("document.body.style.zoom='125%'")
    driver.execute_script("document.body.style.lineHeight = '16px';")

    if "/" in file:
        file = file.split("/")[-1]

    save_location = output_dir + file

    # If the calculated height is within the max height, take one screenshot
    driver.save_screenshot(f"{save_location}.png")
    print(f"[+] Saved {save_location}.png")

    # Quit the driver after taking screenshots
    driver.quit()
    return save_location


def main():
    # Argument parser for file input
    parser = argparse.ArgumentParser("""python3 file-screenshot.py myfile""")
    parser.add_argument("file", action="store", help="myfile", nargs="*")
    parser.add_argument(
        "-O",
        "--output-folder",
        action="store",
        help="Output folder",
        default="./",
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
    parser.add_argument(
        "--split",
        action="store_true",
        help="Split screenshots",
        default=False,
        required=False,
    )
    args = parser.parse_args()

    output_dir = args.output_folder

    # Makes sure that the last char is a `/`
    # If you don't have this and use a `.` (for the CWD)
    # you'll create hidden files

    if output_dir[-1] != "/":
        output_dir = output_dir + "/"

    # checks if there were multiple files or just one
    if type(args.file) is list:
        for file in args.file:
            try:
                print(f"[+] Grabbing screenshot of '{file}'")
                screenshot_loc = screenshot(file, output_dir, args.browser)
            except Exception as e:
                print("Error, likely file is too small or does not exist", e)

    else:
        print(f"[+] Grabbing screenshot of '{args.file}'")
        screenshot_loc = screenshot(args.file, output_dir, args.browser)

    if args.split:
        # Example usage
        max_height = 520  # Set the max height for each split
        screenshot_file = screenshot_loc + ".png"
        split_image_vertically(screenshot_file, max_height, output_dir)
        # Save the split images


if __name__ == "__main__":
    main()
