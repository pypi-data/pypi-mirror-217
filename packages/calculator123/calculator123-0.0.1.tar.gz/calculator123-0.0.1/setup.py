from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A basic calculator package'
LONG_DESCRIPTION = 'A package that allows to build simple calculator operations'

# Setting up
setup(
    name="calculator123",
    version=VERSION,
    author="Vitalija Valentaite",
    author_email="<vitalija.v7@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'calculator', 'mathematics', 'math', 'operations'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
