from setuptools import setup,find_packages
from typing import List

REQUIREMENT_FILE = "requirements.txt"
PROJECT_NAME     = "Backorder Detection"
AUTHOR           = "Abdeljalil"
AUTHOR_EMAIL     = "d.abdeljalil@gmail.com"
VERSION          = "0.0.1"




def get_requirements()->List[str]:
    """
    get_requirements extracts all external packages
    from requirements.txt, and returns a list of these packages
    """
    with open(REQUIREMENT_FILE) as requirements_file:

        requirements_list = requirements_file.readlines()
        requirements      = [req.replace("/n","") for req in requirements_list]

        if "-e ." in requirements: requirements.remove("-e .")
      
        return requirements

setup(
    name             = PROJECT_NAME,
    author           = AUTHOR,
    author_email     = AUTHOR_EMAIL,
    version          = VERSION,
    packages         = find_packages(),
    install_requires = get_requirements()
)

#python setup.py install conda create --name myenv python=3.9 python3 -m venv myenv