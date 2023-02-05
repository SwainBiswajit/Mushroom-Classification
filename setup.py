# In Python, setup.py is a module used to build and distribute Python packages. 
# It typically contains information about the package, such as its name, version, and dependencies, as well as instructions for building and installing the package. 
# This information is used by the pip tool, which is a package manager for Python that allows users to install and manage Python packages from the command line. 
# By running the setup.py file with the pip tool, you can build and distribute your Python package so that others can use it.

from setuptools import find_packages,setup
from typing import List

REQUIREMENT_FILE_NAME="requirements.txt"
HYPHEN_E_DOT = "-e ."


# This function provides all the required libraries for the project.
def get_requirements()->List[str]:
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list

setup(
    name="Mushroom",
    version="0.0.1",
    author="bis",
    author_email="biswajit30swain@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)

