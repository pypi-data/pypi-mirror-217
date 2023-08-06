#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'requests']

test_requirements = ['pytest>=3', ]

setup(
    author="派大星",
    author_email='nocoding@126.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',

    ],
    description="Yapi Python SDK",
    entry_points={
        'console_scripts': [
            'easy_yapi=easy_yapi.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['easy_yapi', 'yapi'],
    name='easy_yapi',
    packages=find_packages(include=['easy_yapi', 'easy_yapi.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nocoding126/easy_yapi',
    version='0.1.1',
    zip_safe=False,
)
