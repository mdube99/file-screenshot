import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="file-screenshot",
    version="0.1",
    author="Mark Dube",
    author_email="mjdube99@gmail.com",
    description="Tool that screenshots files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["selenium", "pillow", "colorama"],
    entry_points={"console_scripts": ["file-screenshot=file_screenshot.main:main"]},
)
