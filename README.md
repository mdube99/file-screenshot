# file-screenshot

File screenshotting tool written in python. In the backend it uses selenium to open the file in a browser then takes a screenshot of it at 125% zoom. Will automatically split into multiple screenshots if the length of the file you want to screenshot is greater than your max screenshot height (default of 1080).

Why? I needed something that made screenshotting a lot of files easier. Are there other tools out there that do this better and probably easier? Maybe, but I wanted to learn more and this does exactly what I need it to.

## Usage

```
python3 file-screenshot.py myfile [-h] [-O OUTPUT_FOLDER] [-B {firefox,chrome}] file

positional arguments:
  file                  myfile

options:
  -h, --help            show this help message and exit
  -O OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        Output folder
  -B {firefox,chrome}, --browser {firefox,chrome}
                        Browser you want to use
  -M MAX_HEIGHT, --max-height MAX_HEIGHT
                        The max height of your screenshot(s)
```

## Installation

Use pipx:

```
pipx install .
```
