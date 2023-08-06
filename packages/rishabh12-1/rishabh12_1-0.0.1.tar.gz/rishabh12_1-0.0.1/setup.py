from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.01'
DESCRIPTION = 'Add or mean of value'
LONG_DESCRIPTION = 'A package that allows to aithrmeatic operations'

# Setting up
setup(
    name="rishabh12_1",
    version=VERSION,
    author="TCG (Rishabh)",
    author_email="<rihabhk1@dewsolutions.in>",
    # description=DESCRIPTION,
    # long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=['python', 'aithrmatics'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
