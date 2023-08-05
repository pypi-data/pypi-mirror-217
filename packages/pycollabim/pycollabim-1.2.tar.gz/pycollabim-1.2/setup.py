from setuptools import setup, find_packages

# Read long description from file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pycollabim",
    version="1.2",
    packages=find_packages(),
    install_requires=['requests'],
    long_description=long_description,
    long_description_content_type="text/markdown",
)