# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

import setuptools
from version import get_version


with open('README.rst') as f:
    readme = f.read()

setuptools.setup(
    name='mlbackend',
    version=get_version(),
    description='machine learning backend framework',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='Antoine Sauray',
    author_email='antoine@hyperplan.io',
    url='https://github.com/hyperplan-io/ml-backend',
    license='MIT',
    packages=[
        'mlbackend',
        'mlbackend.hooks',
    ],
    package_dir={'mlbackend': 'mlbackend/', 'hooks': 'mlbackend/hooks/'},
    include_package_data=True
)

