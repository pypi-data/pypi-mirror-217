from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.0'
DESCRIPTION = 'Package with trained language models in 6 differente languages.'
LONG_DESCRIPTION = 'A package that contains trained models for text classification in six diferent languages.'

# Setting up
setup(
    name="categorium",
    version=VERSION,
    author="Luís Silva",
    author_email="<aluisgonalo022@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'categorium': ['modelos/*/*']
    },
    install_requires=[],
    keywords=['python', 'classification', 'text', 'Categorization','textCategorization','textclassification'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)