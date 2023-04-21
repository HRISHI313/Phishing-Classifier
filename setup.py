from setuptools import find_packages,setup
from typing import List


HYPEN_DOT_E = "-e ."
def get_requirements(file_path:str)-> List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n"," ") for req in requirements]

        if HYPEN_DOT_E in requirements:
            requirements.remove(HYPEN_DOT_E)

    return requirements



# This code block defines the metadata and dependencies for a Python package called "Phishing Classifier"
# using the setuptools package.

setup(
name='Phishing Classifier',
version='0.0.1',
author='Abishek Banerjee',
author_email='abishekbanerjee10@gmail.com',
packages=find_packages(),
install_requires = get_requirements('requirement.txt')
)

