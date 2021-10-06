
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "flutterpy",
    author = "Guillermo Martínez-López",
    author_email = "guillermo.martinez-lopez@tum.de",
    version = "0.0.0",
    description = "Package for the evaluation of wind-induced flutter effects in structures.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/mtnzguillermo/flutterpy",
    python_requires = ">=3.7",
    install_requires = [
        "numpy >= 1.17.4",
        "scipy >= 1.6.3",
        "sympy >= 1.5.1",
        "matplotlib >= 3.2.0"
    ],
    extras_requires = {
        "dev":[
            
        ]
    },
    keywords = "flutter, wind, aeroelasticity",
    packages = find_packages(exclude=("tests","docs")),
    classifiers = [

    ]
)