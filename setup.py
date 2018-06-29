from __future__ import print_function, unicode_literals
from setuptools import setup, find_packages

from distutils.core import setup

__author__ = "danishabdullah"

with open("requirements.txt", 'r') as file:
    requirements = file.readlines()

with open("readme.md", 'r') as file:
    readme = file.read()

with open("LICENSE", 'r') as file:
    license = file.read()

setup(
    name='ghio',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/danishabdullah/ghio',
    install_requires=requirements,
    license=license,
    zip_safe=False,
    keywords='ghio ',
    author='Danish Abdullah',
    author_email='dev@danishabdullah.com',
    description='ghio',
    package_data={
        '': ['requirements.txt', 'readme.md', 'LICENSE']
    },
    entry_points={
        'console_scripts': ['ghio=$Package_name.scripts.cli:cli']
    },
    long_description=readme,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
