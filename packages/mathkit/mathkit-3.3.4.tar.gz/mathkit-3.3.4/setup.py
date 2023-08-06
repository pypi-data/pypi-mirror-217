from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mathkit",
    version="3.3.4",
    author="TheUnkownHacker",
    author_email="theunkownhacker@gmail.com",
    description="Python library for mathematical functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theunkownhacker/mathkit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
