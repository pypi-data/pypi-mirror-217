from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.0'
DESCRIPTION = 'A module to work with python modules'
ld = """This module created for make functions and classes, Then save that into the a file"""
setup (
    name="pfacbuilder",
    version=VERSION,
    author="VenzTechnolo",
    author_email="venztechnolo@gmail.com",
    description=DESCRIPTION,
    long_description=ld,
    packages=find_packages(),
    py_modules=[],
    keywords=["python", "function", "class", "functions", "classes", "python3"],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)