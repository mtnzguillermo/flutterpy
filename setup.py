
from setuptools import setup, find_packages

setup(
    name="flutterpy",
    version="0.1.0",
    description="Package for the evaluation of wind-induced flutter effects in structures.",
    packages=find_packages(exclude=("tests","docs"))
)