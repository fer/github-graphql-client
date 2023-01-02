"""
setup.py
"""

from setuptools import setup

setup(
    name='ghgqlclient',
    version='0.1',
    description='Module for consuming the Github GraphQL API.',
    author='fer',
    author_email='fer@ferqwerty.com',
    packages=['ghgqlclient'],
    install_requires=[
        'numpy',
        'pandas',
    ],
)
