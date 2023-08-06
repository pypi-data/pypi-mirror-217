from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='cryptarithm',
    version='0.1',
    author="dragoemon",
    author_email="dragoemon32@gmail.com",
    description="make cryptarithm in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dragoemon1/cryptarithm",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages()
)