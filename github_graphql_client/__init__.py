import logging
from ratelimit import limits, sleep_and_retry, RateLimitException
from python_graphql_client import GraphqlClient
import ipywidgets as widgets
from IPython.display import clear_output, display

PERIOD                  = 150
MAX_CALLS_PER_MINUTE    = 15

"""
GitHubGraphQLClient

To do:
- implement smart rate limiting and remove `sleep_and_retry`
- get a file content from repo
- get_contents of a file from a repo (catalog.yml, ... check exsistence)
"""
class GitHubGraphQLClient:
    __base_url = 'https://api.github.com/graphql'

    def __init__(self, token, log_file_name):
        self.__logger = logging.getLogger()
        log_str = '%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_str)
        fhandler = logging.FileHandler(filename=log_file_name, mode='a')
        fhandler.setFormatter(formatter)

        self.__logger.addHandler(fhandler)
        self.__logger.setLevel(logging.DEBUG)

        self.__client = GraphqlClient(
            endpoint=self.__base_url,
            headers={'Authorization': f'token {token}'}
        )

        self.__logger.debug(self.__client)

    def _load_query(self, path):
        with open(path) as f:
            return f.read()

    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_MINUTE, period=PERIOD)
    def query(self, graph_ql_file, variables = { 'afterCursor' : None }):
        """
            Regular Query with no pagination
        """
        try:
            return self.__client.execute(
                query = self._load_query(graph_ql_file),
                variables = variables
            )
        except RateLimitException as exception:            
            print(f'Error: {exception}') # fixme: test this.

    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_MINUTE, period=PERIOD)
    def query_pagination(self, graph_ql_filename, variables: dict, verbose = True, debug = False):
        """
            Query with pagination
        """
        has_next_page = True
        after_cursor = None
        page_count = 0
        edges = []

        if verbose:
            progress_bar = widgets.IntProgress(
                min=0,
                max=0,
                description='Loading ...',
                layout=widgets.Layout(width='95%')
            )

            display(progress_bar)

        while (has_next_page):
            variables.update({'afterCursor': after_cursor})
            query_results = self.query(graph_ql_filename, variables)
            batch = query_results['data']

            key_one = list(batch.keys())[0]

            if key_one == 'search':
                batch = batch[key_one]
                if verbose:
                    progress_bar.max = batch['repositoryCount']
            else:
                keyTwo = list(batch[key_one].keys())[0]
                batch = batch[key_one][keyTwo]
                progress_bar.max = batch['totalCount']

            page_count += 1

            # Import edges
            for edge in map(lambda x: x['node'], batch['edges']):
                edges.append(edge)

            if verbose:
                progress_bar.value = len(edges)
                progress_bar.description = f" {len(edges)} / {progress_bar.max} "

            has_next_page = batch['pageInfo']['hasNextPage']
            after_cursor = batch['pageInfo']['endCursor']

            if debug:
                debug_str = f"Edges: {len(edges)} Page Count: {page_count} has_next_page: {has_next_page} after_cursor: {after_cursor}"
                print(debug_str, end="\r")

            clear_output()

            return edges