# pylint: skip-file
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))


# Get the requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt."""
    with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
        requirements = f.read().splitlines()
    return requirements


# This call to setup() does all the work
setup(
    name="waveglowpkg",
    version="0.0.1",
    description="WaveGlow model to generate audio from mel-spectrograms",
    long_description="WaveGlow for Botiverse Package",
    long_description_content_type="text/markdown",
    url="https://waveglow.readthedocs.io/",
    author="Essam",
    author_email="essamwisam@outlook.com",
    license="",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["waveglow"],
    include_package_data=False,
    install_requires=read_requirements(),
)

# Steps to upload to PyPI
# 0 - Increment the version number in setup.py
# 1 - Remove the dist folder
# 2- python3 setup.py sdist bdist_wheel  
# 3 - twine upload dist/*