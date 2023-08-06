from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="Tanki",
    version="1.0.0",
    author="walker",
    description="API wrapper for Tanki Online's ratings API",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=['tanki'],
    url="https://github.com/wa1ker38552/tanki",
    install_requires=["requests"],
    python_requires=">=3.7",
    py_modules=["tanki"]
)