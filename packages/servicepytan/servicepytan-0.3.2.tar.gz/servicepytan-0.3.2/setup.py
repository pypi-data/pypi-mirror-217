#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'requests', 'python-dateutil', 'pytz','python-dotenv','pyyaml']

test_requirements = [ ]

setup(
    author="Elliot Palmer",
    author_email='elliot@ecoplumbers.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Library to make it easier to interact with the ServiceTitan API v2",
    entry_points={
        'console_scripts': [
            'servicepytan=servicepytan.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='servicepytan',
    name='servicepytan',
    packages=find_packages(include=['servicepytan', 'servicepytan.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/elliotpalmer/servicepytan',
    version='0.3.2',
    zip_safe=False,
)
