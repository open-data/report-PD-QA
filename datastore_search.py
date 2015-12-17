import requests

import json
from package_search import PackageSearch

class DataStoreSearch(PackageSearch):

    def __init__(self, base_url, search_url):
        super(DataStoreSearch,self).__init__(base_url, search_url)

    def tables_in_resources(self, resources, api_key):

        tables={}

        for resource in resources:

            params={"resource_id":resource}

            try:
                result = self.get_request(self.search_url,params,api_key)
                tables[resource]=dict([('HTTP_status', 'success'),
                                    ('HTTP_message', 'request success'),
                                    ('records', result['result']['records'])
                                    ])
            except Exception:
                tables[resource]=dict([('HTTP_status', 'error'),
                                    ('HTTP_message',Exception.message)])
            continue

        return tables
