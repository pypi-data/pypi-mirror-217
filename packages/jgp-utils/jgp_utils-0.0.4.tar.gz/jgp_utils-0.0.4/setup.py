import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.4' 
PACKAGE_NAME = 'jgp_utils' 
AUTHOR = 'Sistemas' 
AUTHOR_EMAIL = 'sistemas@jesusgranpoder.com.bo' 
URL = 'https://gitlab.com/jgp-devs2/jgp-lib/jgp-utils'

LICENSE = 'MIT' 
DESCRIPTION = 'Librería con funciones y herramientas útiles'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"


INSTALL_REQUIRES = [
      #'locale'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)