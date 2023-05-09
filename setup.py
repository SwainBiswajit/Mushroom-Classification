from setuptools import find_packages,setup
from typing import List

REQUIREMENTS_FILE = "requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements()->List[str]:
    with open(REQUIREMENTS_FILE) as requirement_file:
        requirements_list = requirement_file.readlines()
    requirements_list = [requirement_name.replace("\n","") for requirement_name in requirements_list]

    if HYPHEN_E_DOT in requirements_list:
        requirements_list.remove(HYPHEN_E_DOT)
    return requirements_list    

setup(
    name="Mushroom_classification",
    version="0.0.1",
    author="Biswajit",
    author_email="biswajit30swain@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)