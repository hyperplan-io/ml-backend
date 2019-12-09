# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='mlbackend',
    version='0.1.0-test',
    description='machine learning backend framework',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='Antoine Sauray',
    author_email='sauray.antoine@outlook.com',
    url='https://github.com/hyperplan-io/ml-backend',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs'))
)

