# -*- coding: utf-8 -*-
import sys
import pathlib
from pkg_resources import VersionConflict, require
from setuptools import setup, find_packages

try:
    require('setuptools>=38.3')
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)

BASE_DIR = pathlib.Path(__file__).parent

PACKAGE_NAME = "wb_cleaning"
VERSION = "0.0.1"
AUTHOR = "Aivin V. Solatorio"
AUTHOR_EMAIL = "avsolatorio@gmail.com"
URL = "https://github.com/worldbank/wb-nlp-tools"

LICENSE = "MIT"
DESCRIPTION = 'Python package containing the implementation of a customizable text cleaning pipeline.'
LONG_DESCRIPTION = (BASE_DIR / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python"
]
INSTALL_REQUIRES = [
    "unidecode",
    "inflect==5.3.0",
    "fasttext",
    "polyglot",
    "PyICU",
    "flashtext>=2.7,<3.0.0",
    "openpyxl==3.0.7",
    "spacy>=2.3.5,<=2.3.7",
    "numpy>=1.21.0,<=1.21.5",
    "spacy-langdetect==0.1.2",
    "wordninja==2.0.0",
    "pandas>=1.1.2,<=1.2.0",
    "pyenchant>=3.1.1,<=3.2.0",
    "scipy>1.5.2,<=1.5.4",
    "nltk>=3.5,<=3.6.2",
    "scikit-learn>0.23.2,<=0.24.0",
    "redis==3.5.3",
    "joblib>0.16.0,<=1.0.0",
    "bs4<=4.9.1",
    "requests>2.24.0,<=2.25.1",
    "tika==1.24",
    "googletrans==3.1.0a0"]
DEPENDENCY_LINKS=[
    "git+https://github.com/avsolatorio/pycld2.git@d63195032c3a2c126cc4cbe1cb1c6de8cf8c8d2a"]
PACKAGE_DIR = {'': 'src'}

# Setting up
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    license=LICENSE,
    url=URL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    install_requires=INSTALL_REQUIRES,
    dependency_link=DEPENDENCY_LINKS,
    classifiers=CLASSIFIERS,
    package_dir=PACKAGE_DIR,
    packages=find_packages(include=['wb_cleaning'])
)
