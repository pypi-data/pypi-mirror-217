""""
Setup-File
Authors: Judith von Bornhaupt, Markus Bartl
Date: June 2023
"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

with open('requirements.txt', 'r', encoding='utf-8') as requirements_file:
    requirements = requirements_file.readlines()


setup(
    name='ensemble_regressor',
    author='Judith von Bornhaupt & Markus Bartl',
    author_email='2210837780@stud.fh-kufstein.ac.at, 2210837729@stud.fh-kufstein.ac.at',
    version='1.0.0',
    description='Ensemble Regressor Package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.fh-kufstein.ac.at',
    requires=["numpy","matplotlib","setuptools"],
    packages=find_packages()
)
