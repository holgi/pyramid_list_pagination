#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The setup script.'''

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'SQLAlchemy']

setup(
    author='Holger Frey',
    author_email='mail@holgerfrey.de',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.6',
        'Framework :: Pyramid'
    ],
    description='Pyramid Listing contains pyramid resources and helpers for pagination of result lists',
    install_requires=requirements,
    license='Beerware',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyramid list pagination resource',
    name='pyramid_listing',
    packages=find_packages(include=['pyramid_listing']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/holgi/pyramid_listing',
    version='0.1.1',
    zip_safe=False,
)
