# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='mlbackend',
    version='0.1.0',
    description='Machine Learning Backend Framework',
    long_description=readme,
    author='Antoine Sauray',
    author_email='sauray.antoine@outlook.com',
    url='https://github.com/hyperplan-io/ml-backend',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

