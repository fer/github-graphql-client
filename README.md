# github-graphql-client

Module for consuming [Github GraphQL API](https://docs.github.com/en/graphql) in Python.


## Install

```bash
pip install git+https://github.com/fer/github-graphql-client.git
```

## Usage

Get your Personal access tokens from [GitHub](https://github.com/settings/tokens).

```python
from github_graphql_client import GitHubGraphQLClient

ACCESS_TOKEN = '<your_access_token>' 

gh_gql = GitHubGraphQLClient(ACCESS_TOKEN, './logs/GitHubGraphQLClient.log')
```

Query without pagination:

```python
rate_limit = gh_gql.query(
    'graphql/GitHub/get-ratelimit.graphql'
)['data']['rateLimit']
```

Query with pagination:

```python
import pandas as pd

TERM = 'poc-'

print(f"Searching for '{TERM}' repos...")    

repos = gh_gql.query_pagination(
    'graphql/GitHub/search-repos-query.graphql', 
    {
        'queryString': f'org:backbase-rnd {TERM}'
    }
)

df = pd.DataFrame(repos)
```