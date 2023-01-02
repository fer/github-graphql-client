"""
setup.py
"""

from setuptools import setup

setup(
    name='github_graphql_client',
    version='0.1',
    description='Module for consuming the Github GraphQL API.',
    author='fer',
    author_email='fer@ferqwerty.com',
    packages=['github_graphql_client'],
    install_requires=[
        'numpy',
        'pandas',
    ],
)
