"""
setup.py
"""

from setuptools import setup

setup(
    name='GitHubGraphQLClient',
    version='0.1',
    description='Module for consuming the Github GraphQL API.',
    author='fer',
    author_email='fer@ferqwerty.com',
    packages=['GitHubGraphQLClient'],
    install_requires=[
        'numpy',
        'pandas',
    ],
)
