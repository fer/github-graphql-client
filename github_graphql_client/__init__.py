"""
GitHubGraphQLClient

To do:
- implement smart rate limiting and remove `sleep_and_retry`
- get a file content from repo
- get_contents of a file from a repo (catalog.yml, ... check exsistence)
"""

from ratelimit import limits, sleep_and_retry, RateLimitException
from python_graphql_client import GraphqlClient
from IPython.display import clear_output, display

class GitHubGraphQLClient:
    """A dummy docstring."""

    def main(self):
        """A dummy docstring."""
        print('Whatever')
